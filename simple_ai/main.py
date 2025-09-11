def get_response(user_input):
    """
    Gets a response from the AI based on a set of rules.
    """
    # Convert user input to lowercase to make the matching case-insensitive
    lowered_input = user_input.lower()

    # Define the rules as a dictionary. We check for keywords.
    rules = {
        "hola": "¡Hola! Soy tu asistente. ¿En qué te puedo ayudar?",
        "como estas": "Soy un programa, así que siempre estoy al 100%. ¿Y tú?",
        "que puedes hacer": "Por ahora, puedo responder a saludos y preguntas simples. ¡Estoy aprendiendo!",
        "adios": "¡Hasta pronto!"
    }

    # Iterate through the rules to find a matching keyword in the user's input.
    for keyword, response in rules.items():
        if keyword in lowered_input:
            return response

    # Default response if no rule matches.
    return "Lo siento, no te he entendido. Todavía estoy en desarrollo."

def main():
    """
    Main function to run the AI chat application.
    """
    print("AI Asistente Iniciado. Escribe 'adios' para salir.")
    print("-" * 50)

    while True:
        try:
            user_input = input("Tú: ")

            # The "adios" keyword is handled in the rules, but we can also use it to break the loop.
            if "adios" in user_input.lower():
                print("Asistente: ¡Hasta pronto!")
                break

            response = get_response(user_input)
            # The get_response function will handle the "adios" response, so we just print it.
            print(f"Asistente: {response}")

        except KeyboardInterrupt:
            print("\nAsistente: ¡Hasta pronto!")
            break

if __name__ == "__main__":
    main()
