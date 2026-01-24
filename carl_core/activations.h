#ifndef ACTIVATIONS_H
#define ACTIVATIONS_H

#include <math.h>

// Sigmoid activation function
static inline double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}

// Derivative of the sigmoid function.
// NOTE: The input 'x' is assumed to be the *output* of the sigmoid function.
static inline double sigmoid_derivative(double x) {
    return x * (1.0 - x);
}

#endif // ACTIVATIONS_H
