import random
import math
from python_interface.carl import NeuralNetwork, Matrix

def main():
    # --- 1. Define el problema y la configuración de la red ---
    topology = [2, 3, 1]
    nn = NeuralNetwork(topology)

    # Datos de entrenamiento para el problema XOR
    training_data = [
        {'input': [0.0, 0.0], 'target': [0.0]},
        {'input': [0.0, 1.0], 'target': [1.0]},
        {'input': [1.0, 0.0], 'target': [1.0]},
        {'input': [1.0, 1.0], 'target': [0.0]},
    ]

    # Hiperparámetros
    epochs = 10000
    learning_rate = 0.1

    print(f"Entrenando la red con topología {topology} durante {epochs} épocas...")

    # --- 2. Bucle de Entrenamiento ---
    for epoch in range(epochs):
        # Seleccionar un dato de entrenamiento al azar en cada época
        data_point = random.choice(training_data)

        input_matrix = Matrix.from_list([data_point['input']])
        target_matrix = Matrix.from_list([data_point['target']])

        # Realizar un paso de entrenamiento
        nn.train(input_matrix, target_matrix, learning_rate)

        # --- 3. Calcular y mostrar el error (opcional, pero útil) ---
        if (epoch + 1) % 1000 == 0:
            total_error = 0
            for data in training_data:
                input_mat = Matrix.from_list([data['input']])
                target_mat = Matrix.from_list([data['target']])

                prediction_mat = nn.forward(input_mat)

                # Calcular el error cuadrático (target - prediction)^2
                error_mat = Matrix.from_list([[
                    target_mat.to_list()[0][0] - prediction_mat.to_list()[0][0]
                ]])
                total_error += math.pow(error_mat.to_list()[0][0], 2)

            # Imprimir el Error Cuadrático Medio (MSE)
            mse = total_error / len(training_data)
            print(f"Época: {epoch + 1}/{epochs}, Error Cuadrático Medio: {mse:.6f}")

    # --- 4. Verificación final ---
    print("\n--- Resultados después del entrenamiento ---")
    for data in training_data:
        input_m = Matrix.from_list([data['input']])
        prediction = nn.forward(input_m).to_list()[0][0]
        print(f"Entrada: {data['input']} -> Predicción: {prediction:.4f} (Esperado: {data['target'][0]})")

if __name__ == "__main__":
    main()
