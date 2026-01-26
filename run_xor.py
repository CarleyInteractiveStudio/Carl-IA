from python_interface.carl import NeuralNetwork, Matrix

def main():
    """
    Initializes a neural network and runs the XOR inputs through it
    to demonstrate that the forward propagation mechanism works.

    Note: The network is not trained, so the output will be random,
    not the correct XOR result.
    """

    # Define the topology for the XOR problem:
    # 2 input neurons (for x1 and x2)
    # 3 neurons in a hidden layer
    # 1 output neuron
    topology = [2, 3, 1]

    print(f"Creating a Neural Network with topology: {topology}")
    nn = NeuralNetwork(topology)

    # Define the XOR input data
    xor_inputs = [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0]
    ]

    print("\n--- Running Forward Propagation for XOR Inputs ---")

    for input_data in xor_inputs:
        # Create a 1x2 matrix for the input
        input_matrix = Matrix.from_list([input_data])

        # Perform the forward pass
        output_matrix = nn.forward(input_matrix)

        # Convert the output matrix to a Python list to display it
        output_data = output_matrix.to_list()

        print(f"Input: {input_data} -> Output: {output_data[0][0]:.4f}")

if __name__ == "__main__":
    main()
