#ifndef EMBEDDING_LAYER_H
#define EMBEDDING_LAYER_H

#include "matrix.h"

// Represents an embedding layer, which is essentially a lookup table.
typedef struct {
    Matrix* embeddings; // Each row is a vector for a token.
} EmbeddingLayer;

// Creates a new embedding layer.
// vocab_size: The number of unique tokens in the vocabulary.
// embedding_dim: The size of the embedding vector for each token.
EmbeddingLayer* embedding_layer_create(int vocab_size, int embedding_dim);

// Frees the memory allocated for the embedding layer.
void embedding_layer_destroy(EmbeddingLayer* layer);

// Performs a forward pass through the embedding layer.
// Takes an array of token IDs and returns a matrix of their corresponding vectors.
Matrix* embedding_layer_forward(const EmbeddingLayer* layer, const int* token_ids, int sequence_length);

#endif // EMBEDDING_LAYER_H
