#ifndef MATRIX_H
#define MATRIX_H

#include <stdlib.h>

// Represents a 2D Matrix
typedef struct {
    int rows;
    int cols;
    double** data;
} Matrix;

// Function declarations for matrix operations

// Creates a new matrix with the given dimensions
Matrix* matrix_create(int rows, int cols);

// Creates a matrix with sinusoidal positional encodings
Matrix* matrix_create_positional_encoding(int max_len, int d_model);

// Frees the memory allocated for a matrix
void matrix_destroy(Matrix* m);

// Initializes a matrix with random values between -1.0 and 1.0
void matrix_randomize(Matrix* m);

// Prints the matrix to the console (for debugging)
void matrix_print(const Matrix* m);

// Performs matrix multiplication: C = A * B
Matrix* matrix_multiply(const Matrix* a, const Matrix* b);

// Adds a bias vector to each row of the matrix
void matrix_add_bias(Matrix* m, const Matrix* bias);

// Applies a function element-wise to the matrix
void matrix_map(Matrix* m, double (*func)(double));

// Creates a deep copy of a matrix
Matrix* matrix_copy(const Matrix* src);

// Subtracts matrix B from matrix A and returns the result as a new matrix
Matrix* matrix_subtract(const Matrix* a, const Matrix* b);

// Adds matrix B to matrix A and returns the result as a new matrix
Matrix* matrix_add(const Matrix* a, const Matrix* b);

// Transposes a matrix
Matrix* matrix_transpose(const Matrix* m);

// Performs element-wise multiplication (Hadamard product)
Matrix* matrix_elementwise_multiply(const Matrix* a, const Matrix* b);

// Multiplies every element of a matrix by a scalar value.
void matrix_scale(Matrix* m, double scalar);

// Applies the softmax function to each row of the matrix.
void matrix_softmax(Matrix* m);

#endif // MATRIX_H
