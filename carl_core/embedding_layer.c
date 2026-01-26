#include "embedding_layer.h"
#include <stdio.h>
#include <stdlib.h>

EmbeddingLayer* embedding_layer_create(int vocab_size, int embedding_dim) {
    EmbeddingLayer* layer = (EmbeddingLayer*)malloc(sizeof(EmbeddingLayer));
    if (!layer) {
        fprintf(stderr, "Error: Could not allocate memory for EmbeddingLayer.\n");
        return NULL;
    }

    // The embedding table is a matrix where rows = vocab_size and cols = embedding_dim
    layer->embeddings = matrix_create(vocab_size, embedding_dim);
    if (!layer->embeddings) {
        free(layer);
        return NULL;
    }

    // Initialize embeddings with small random values
    matrix_randomize(layer->embeddings);

    return layer;
}

void embedding_layer_destroy(EmbeddingLayer* layer) {
    if (!layer) return;
    matrix_destroy(layer->embeddings);
    free(layer);
}

Matrix* embedding_layer_forward(const EmbeddingLayer* layer, const int* token_ids, int sequence_length) {
    if (!layer || !token_ids) return NULL;

    int embedding_dim = layer->embeddings->cols;

    // Create the output matrix: rows = sequence_length, cols = embedding_dim
    Matrix* output = matrix_create(sequence_length, embedding_dim);
    if (!output) return NULL;

    // For each token ID in the input sequence, copy the corresponding vector
    for (int i = 0; i < sequence_length; i++) {
        int token_id = token_ids[i];

        // Check for out-of-bounds access
        if (token_id < 0 || token_id >= layer->embeddings->rows) {
            fprintf(stderr, "Error: Token ID %d is out of vocabulary bounds.\n", token_id);
            matrix_destroy(output);
            return NULL;
        }

        // Copy the vector from the embedding table to the output matrix
        for (int j = 0; j < embedding_dim; j++) {
            output->data[i][j] = layer->embeddings->data[token_id][j];
        }
    }

    return output;
}
