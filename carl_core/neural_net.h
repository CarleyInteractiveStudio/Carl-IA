#ifndef NEURAL_NET_H
#define NEURAL_NET_H

#include "matrix.h"

// Represents a single layer in the neural network
typedef struct {
    Matrix* weights; // Matrix of weights for the connections to the previous layer
    Matrix* biases;  // Vector of biases for each neuron in this layer
} Layer;

// Represents the entire neural network
typedef struct {
    int num_layers;
    int* topology; // Array defining the number of neurons in each layer (e.g., [2, 3, 1])
    Layer* layers; // Array of layers
} NeuralNetwork;

// --- Function Declarations ---

// Creates and initializes a new neural network based on a given topology
NeuralNetwork* nn_create(const int* topology, int num_layers);

// Frees all memory associated with the neural network
void nn_destroy(NeuralNetwork* nn);

// Performs forward propagation through the entire network
Matrix* nn_forward(NeuralNetwork* nn, const Matrix* input);

// Prints the network structure and weights (for debugging)
void nn_print(const NeuralNetwork* nn);


#endif // NEURAL_NET_H
