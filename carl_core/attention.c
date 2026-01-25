#include "attention.h"
#include <math.h>
#include <stdio.h>

Matrix* scaled_dot_product_attention(const Matrix* query, const Matrix* key, const Matrix* value) {
    // K^T
    Matrix* key_transposed = matrix_transpose(key);
    if (!key_transposed) return NULL;

    // Q * K^T
    Matrix* scores = matrix_multiply(query, key_transposed);
    matrix_destroy(key_transposed); // No longer needed
    if (!scores) return NULL;

    // Scaling factor: sqrt(d_k) where d_k is the dimension of the key vectors
    double scale_factor = sqrt((double)key->cols);
    if (scale_factor == 0) {
        fprintf(stderr, "Error: Cannot divide by zero; key dimension is zero.\n");
        matrix_destroy(scores);
        return NULL;
    }

    // scores / sqrt(d_k)
    matrix_scale(scores, 1.0 / scale_factor);

    // softmax(scores)
    matrix_softmax(scores);

    // result = softmax_scores * V
    Matrix* result = matrix_multiply(scores, value);
    matrix_destroy(scores); // No longer needed

    return result;
}
