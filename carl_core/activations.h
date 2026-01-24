#ifndef ACTIVATIONS_H
#define ACTIVATIONS_H

#include <math.h>

// Sigmoid activation function
static inline double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}

// Derivative of the sigmoid function (will be needed for backpropagation later)
static inline double sigmoid_derivative(double x) {
    double s = sigmoid(x);
    return s * (1.0 - s);
}

#endif // ACTIVATIONS_H
