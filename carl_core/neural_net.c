#include "neural_net.h"
#include "activations.h"
#include <stdio.h>
#include <string.h> // For memcpy

NeuralNetwork* nn_create(const int* topology, int num_layers) {
    if (num_layers < 2) {
        fprintf(stderr, "Error: A neural network must have at least 2 layers (input and output).\n");
        return NULL;
    }

    NeuralNetwork* nn = (NeuralNetwork*)malloc(sizeof(NeuralNetwork));
    if (!nn) return NULL;

    nn->num_layers = num_layers;
    nn->topology = (int*)malloc(num_layers * sizeof(int));
    if (!nn->topology) {
        free(nn);
        return NULL;
    }
    memcpy(nn->topology, topology, num_layers * sizeof(int));

    // We have num_layers - 1 sets of weights and biases
    nn->layers = (Layer*)malloc((num_layers - 1) * sizeof(Layer));
    if (!nn->layers) {
        free(nn->topology);
        free(nn);
        return NULL;
    }

    // Initialize each layer (from the first hidden layer to the output layer)
    for (int i = 0; i < num_layers - 1; i++) {
        int input_size = topology[i];
        int output_size = topology[i + 1];

        // Create weights matrix and biases vector for the current layer
        nn->layers[i].weights = matrix_create(input_size, output_size);
        nn->layers[i].biases = matrix_create(1, output_size);

        // Check for allocation failure and perform robust cleanup
        if (!nn->layers[i].weights || !nn->layers[i].biases) {
            fprintf(stderr, "Error: Failed to allocate memory for layer %d.\n", i);
            // Free all previously allocated layers
            for (int j = 0; j <= i; j++) {
                matrix_destroy(nn->layers[j].weights);
                matrix_destroy(nn->layers[j].biases);
            }
            free(nn->layers);
            free(nn->topology);
            free(nn);
            return NULL;
        }

        // Randomize the weights and biases
        matrix_randomize(nn->layers[i].weights);
        matrix_randomize(nn->layers[i].biases);
    }

    return nn;
}

void nn_destroy(NeuralNetwork* nn) {
    if (!nn) return;

    for (int i = 0; i < nn->num_layers - 1; i++) {
        matrix_destroy(nn->layers[i].weights);
        matrix_destroy(nn->layers[i].biases);
    }

    free(nn->layers);
    free(nn->topology);
    free(nn);
}

Matrix* nn_forward(NeuralNetwork* nn, const Matrix* input) {
    // The 'current_output' matrix will be passed from one layer to the next.
    // We start with a copy of the input.
    Matrix* current_output = matrix_copy(input);
    if (!current_output) return NULL;

    for (int i = 0; i < nn->num_layers - 1; i++) {
        Matrix* prev_output = current_output;

        // Multiply the output of the previous layer by the weights of the current layer
        current_output = matrix_multiply(prev_output, nn->layers[i].weights);

        // Add the bias
        matrix_add_bias(current_output, nn->layers[i].biases);

        // Apply the activation function
        matrix_map(current_output, sigmoid);

        // Free the matrix from the previous step
        matrix_destroy(prev_output);

        // If any step failed, stop and return NULL
        if (!current_output) {
            fprintf(stderr, "Error during forward propagation at layer %d.\n", i);
            return NULL;
        }
    }

    return current_output;
}

void nn_print(const NeuralNetwork* nn) {
    if (!nn) {
        printf("Neural Network is NULL.\n");
        return;
    }

    printf("Neural Network Topology: ");
    for (int i = 0; i < nn->num_layers; i++) {
        printf("%d", nn->topology[i]);
        if (i < nn->num_layers - 1) printf(" -> ");
    }
    printf("\n");

    for (int i = 0; i < nn->num_layers - 1; i++) {
        printf("\n--- Layer %d ---\n", i);
        printf("Weights Matrix:\n");
        matrix_print(nn->layers[i].weights);
        printf("\nBiases Vector:\n");
        matrix_print(nn->layers[i].biases);
    }
}
