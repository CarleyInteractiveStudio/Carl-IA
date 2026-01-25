#ifndef ATTENTION_H
#define ATTENTION_H

#include "matrix.h"

// Calculates Scaled Dot-Product Attention.
// Q, K, and V are the Query, Key, and Value matrices.
// Returns a new matrix with the attention output.
Matrix* scaled_dot_product_attention(const Matrix* query, const Matrix* key, const Matrix* value);

#endif // ATTENTION_H
