#ifndef TRANSFORMER_BLOCK_H
#define TRANSFORMER_BLOCK_H

#include "matrix.h"
#include "neural_net.h"

// Represents a single Transformer Block, combining self-attention and a feed-forward network.
typedef struct {
    // Parameters for the self-attention mechanism
    Matrix* Wq; // Weight matrix for Query
    Matrix* Wk; // Weight matrix for Key
    Matrix* Wv; // Weight matrix for Value

    // Feed-forward neural network part of the block
    NeuralNetwork* ffn;
} TransformerBlock;

// --- Function Declarations ---

// Creates and initializes a new Transformer Block.
// - input_dim: The dimension of the input vectors (e.g., embedding dimension).
// - ffn_hidden_dim: The dimension of the hidden layer in the feed-forward network.
TransformerBlock* transformer_block_create(int input_dim, int ffn_hidden_dim);

// Frees all memory associated with the Transformer Block.
void transformer_block_destroy(TransformerBlock* block);

// Performs a forward pass through the Transformer Block.
// - input: A matrix where each row is an input vector.
Matrix* transformer_block_forward(const TransformerBlock* block, const Matrix* input);

#endif // TRANSFORMER_BLOCK_H
