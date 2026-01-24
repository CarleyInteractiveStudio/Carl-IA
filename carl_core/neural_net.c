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

// Helper function to apply the derivative of the sigmoid function element-wise
void matrix_map_sigmoid_derivative(Matrix* m) {
    for (int i = 0; i < m->rows; i++) {
        for (int j = 0; j < m->cols; j++) {
            m->data[i][j] = sigmoid_derivative(m->data[i][j]);
        }
    }
}

void nn_train(NeuralNetwork* nn, const Matrix* input, const Matrix* target, double learning_rate) {
    // --- 1. Forward Pass ---
    // We need to store the outputs of each layer for backpropagation
    Matrix** layer_outputs = (Matrix**)malloc(nn->num_layers * sizeof(Matrix*));
    layer_outputs[0] = matrix_copy(input);

    for (int i = 0; i < nn->num_layers - 1; i++) {
        Matrix* prev_output = layer_outputs[i];
        Matrix* current_output = matrix_multiply(prev_output, nn->layers[i].weights);
        matrix_add_bias(current_output, nn->layers[i].biases);
        matrix_map(current_output, sigmoid);
        layer_outputs[i + 1] = current_output;
    }

    // --- 2. Backpropagation ---
    // Calculate the error for the output layer
    Matrix* output_error = matrix_subtract(target, layer_outputs[nn->num_layers - 1]);

    // Loop backwards from the last layer to the first hidden layer
    for (int i = nn->num_layers - 2; i >= 0; i--) {
        // Calculate gradient (delta rule)
        Matrix* gradients = matrix_copy(layer_outputs[i + 1]);
        matrix_map_sigmoid_derivative(gradients); // This is f'(net)

        // Multiply by error to get the final delta
        Matrix* temp_gradients = gradients;
        gradients = matrix_elementwise_multiply(temp_gradients, output_error);
        matrix_destroy(temp_gradients); // Clean up the intermediate matrix

        // Calculate deltas
        Matrix* layer_outputs_transposed = matrix_transpose(layer_outputs[i]);
        Matrix* deltas = matrix_multiply(layer_outputs_transposed, gradients);

        // Update weights and biases
        for (int r = 0; r < deltas->rows; r++) {
            for (int c = 0; c < deltas->cols; c++) {
                nn->layers[i].weights->data[r][c] += deltas->data[r][c] * learning_rate;
            }
        }
        for (int r = 0; r < gradients->rows; r++) {
            for (int c = 0; c < gradients->cols; c++) {
                 nn->layers[i].biases->data[r][c] += gradients->data[r][c] * learning_rate;
            }
        }

        // Calculate the error for the previous layer (for the next iteration)
        Matrix* prev_error = matrix_transpose(nn->layers[i].weights);
        Matrix* next_output_error = matrix_multiply(gradients, prev_error);

        // Cleanup intermediate matrices.
        // Crucially, we must store the old error pointer before updating it,
        // to prevent a use-after-free bug.
        Matrix* old_error = output_error;
        output_error = next_output_error;
        matrix_destroy(old_error);

        matrix_destroy(gradients);
        matrix_destroy(layer_outputs_transposed);
        matrix_destroy(deltas);
        matrix_destroy(prev_error);
    }

    // Final cleanup
    matrix_destroy(output_error);
    for (int i = 0; i < nn->num_layers; i++) {
        matrix_destroy(layer_outputs[i]);
    }
    free(layer_outputs);
}

void nn_save(const NeuralNetwork* nn, const char* filepath) {
    FILE* file = fopen(filepath, "wb");
    if (!file) {
        fprintf(stderr, "Error: Could not open file for writing: %s\n", filepath);
        return;
    }

    // Write the topology (number of layers and neuron counts)
    fwrite(&nn->num_layers, sizeof(int), 1, file);
    fwrite(nn->topology, sizeof(int), nn->num_layers, file);

    // Write the weights and biases for each layer
    for (int i = 0; i < nn->num_layers - 1; i++) {
        Matrix* weights = nn->layers[i].weights;
        Matrix* biases = nn->layers[i].biases;
        for (int r = 0; r < weights->rows; r++) {
            fwrite(weights->data[r], sizeof(double), weights->cols, file);
        }
        for (int r = 0; r < biases->rows; r++) {
            fwrite(biases->data[r], sizeof(double), biases->cols, file);
        }
    }

    fclose(file);
}

NeuralNetwork* nn_load(const char* filepath) {
    FILE* file = fopen(filepath, "rb");
    if (!file) {
        fprintf(stderr, "Error: Could not open file for reading: %s\n", filepath);
        return NULL;
    }

    // Read the topology
    int num_layers;
    fread(&num_layers, sizeof(int), 1, file);
    int* topology = (int*)malloc(num_layers * sizeof(int));
    fread(topology, sizeof(int), num_layers, file);

    // Create a new network with the loaded topology (without randomizing weights)
    NeuralNetwork* nn = nn_create(topology, num_layers);
    free(topology); // nn_create makes its own copy
    if (!nn) {
        fclose(file);
        return NULL;
    }

    // Read the weights and biases
    for (int i = 0; i < nn->num_layers - 1; i++) {
        Matrix* weights = nn->layers[i].weights;
        Matrix* biases = nn->layers[i].biases;
        for (int r = 0; r < weights->rows; r++) {
            fread(weights->data[r], sizeof(double), weights->cols, file);
        }
        for (int r = 0; r < biases->rows; r++) {
            fread(biases->data[r], sizeof(double), biases->cols, file);
        }
    }

    fclose(file);
    return nn;
}
