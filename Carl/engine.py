# engine.py
from rules import (
    LearnNameRule, AskNameRule, LikeRule, DislikeRule,
    ShowLikesRule, FarewellRule
)

class CarlEngine:
    def __init__(self, memory):
        self.memory = memory
        self.rules = [
            LearnNameRule(),
            AskNameRule(),
            LikeRule(),
            DislikeRule(),
            ShowLikesRule(),
            FarewellRule()
        ]

    def process(self, query):
        for rule in self.rules:
            if rule.match(query):
                return rule.respond(query, self.memory)
        return "No entiendo esa frase. Sigo aprendiendo."
