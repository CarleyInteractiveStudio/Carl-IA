import json
from pathlib import Path

class MemoryManager:
    def __init__(self, path="celebro1/memoria.json"):
        self.path = Path(path)
        self.data = self._load()

    def _load(self):
        if self.path.exists():
            try:
                raw = self.path.read_text(encoding="utf-8")
                obj = json.loads(raw)
                # Asegurarnos de que sea un dict; si no, lo reiniciamos
                if not isinstance(obj, dict):
                    print("⚠️ Memoria corrupta o no es un dict. Se reinicializa.")
                    return {}
                return obj
            except json.JSONDecodeError:
                print("⚠️ JSON inválido. Se reinicializa la memoria.")
                return {}
        # Si no existe, empezamos con dict vacío
        return {}

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.data, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        # Aseguramos que self.data sea un dict
        if not isinstance(self.data, dict):
            self.data = {}
        self.data[key] = value
        self.save()

    def append(self, key, value):
        if not isinstance(self.data, dict):
            self.data = {}
        self.data.setdefault(key, [])
        if value not in self.data[key]:
            self.data[key].append(value)
            self.save()