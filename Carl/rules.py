# rules.py
import re

class Rule:
    def match(self, query): ...
    def respond(self, query, memory): ...

class LearnNameRule(Rule):
    pattern = re.compile(r'tu nombre es\s+([\wáéíóúñ]+)', re.I)

    def match(self, query):
        return bool(self.pattern.search(query))

    def respond(self, query, memory):
        name = self.pattern.search(query).group(1).capitalize()
        memory.set('name', name)
        return f"Entendido. Ahora me llamo {name}."

class AskNameRule(Rule):
    triggers = ['cómo te llamas', 'cuál es tu nombre']

    def match(self, query):
        return any(t in query.lower() for t in self.triggers)

    def respond(self, query, memory):
        name = memory.get('name')
        if name:
            return f"Mi nombre es {name}."
        return "No tengo un nombre. ¿Cómo quieres que me llame?"

class LikeRule(Rule):
    pattern = re.compile(r'me gusta\s+(.+)', re.I)

    def match(self, query):
        return bool(self.pattern.search(query))

    def respond(self, query, memory):
        item = self.pattern.search(query).group(1).strip().lower()
        memory.append('likes', item)
        return f"¡Genial! He anotado que te gusta {item}."

class DislikeRule(Rule):
    pattern = re.compile(r'no me gusta\s+(.+)', re.I)

    def match(self, query):
        return bool(self.pattern.search(query))

    def respond(self, query, memory):
        item = self.pattern.search(query).group(1).strip().lower()
        memory.append('dislikes', item)
        return f"Entendido, no te gusta {item}."

class ShowLikesRule(Rule):
    triggers = ['qué te gusta', 'tus gustos']

    def match(self, query):
        return any(t in query.lower() for t in self.triggers)

    def respond(self, query, memory):
        likes = memory.get('likes', [])
        if likes:
            return "Me gusta " + ", ".join(likes) + "."
        return "Todavía no sé qué me gusta."

class FarewellRule(Rule):
    def match(self, query):
        return query.lower().strip() in ('adiós', 'adios')

    def respond(self, query, memory):
        return "Hasta luego. Ha sido un placer hablar contigo."