#ifndef TRANSFORMER_MODEL_H
#define TRANSFORMER_MODEL_H

#include "embedding_layer.h"
#include "transformer_block.h"
#include "matrix.h"

// Represents the full Transformer (decoder-only) model.
typedef struct {
    int vocab_size;
    int d_model;
    int num_blocks;
    int max_len;

    EmbeddingLayer* embedding_layer;
    Matrix* positional_encoding;
    TransformerBlock** blocks; // Array of pointers to TransformerBlock
} TransformerModel;

// --- Function Declarations ---

// Creates and initializes a new Transformer model.
TransformerModel* transformer_model_create(int vocab_size, int d_model, int num_blocks, int max_len, int ffn_hidden_dim);

// Frees all memory associated with the Transformer model.
void transformer_model_destroy(TransformerModel* model);

// Performs a forward pass through the entire Transformer model.
// - token_ids: An array of integer token IDs representing the input sequence.
// - sequence_length: The number of tokens in the input sequence.
Matrix* transformer_model_forward(const TransformerModel* model, const int* token_ids, int sequence_length);

#endif // TRANSFORMER_MODEL_H
