# carl.py
from memory import MemoryManager
from engine import CarlEngine

def main():
    memory = MemoryManager()
    engine = CarlEngine(memory)

    print("--- Carl v0.2: Aprendizaje de Preferencias ---")
    print("Escribe 'adiós' para salir.\n")

    while True:
        try:
            q = input("Tú: ").strip()
            if not q:
                continue
            resp = engine.process(q)
            print(f"Carl: {resp}")
            if resp.startswith("Hasta luego"):
                break
        except (KeyboardInterrupt, EOFError):
            print("\nCarl: Desconectando. ¡Adiós!")
            break

if __name__ == "__main__":
    main()