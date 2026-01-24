#ifndef ACTIVATIONS_H
#define ACTIVATIONS_H

#include <math.h>

// Enum to identify activation functions
typedef enum {
    SIGMOID,
    RELU
} ActivationType;

// --- Sigmoid ---
static inline double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}
// Derivative of sigmoid (input x is the sigmoid output)
static inline double sigmoid_derivative(double x) {
    return x * (1.0 - x);
}

// --- ReLU (Rectified Linear Unit) ---
static inline double relu(double x) {
    return x > 0 ? x : 0;
}
// Derivative of ReLU
static inline double relu_derivative(double x) {
    return x > 0 ? 1 : 0;
}

#endif // ACTIVATIONS_H
