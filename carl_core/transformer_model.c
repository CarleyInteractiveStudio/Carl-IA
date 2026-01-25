#include <stdio.h>
#include <stdlib.h>
#include "transformer_model.h"

TransformerModel* transformer_model_create(int vocab_size, int d_model, int num_blocks, int max_len, int ffn_hidden_dim) {
    TransformerModel* model = (TransformerModel*)malloc(sizeof(TransformerModel));
    if (!model) {
        fprintf(stderr, "Error: Failed to allocate memory for TransformerModel.\n");
        return NULL;
    }

    model->vocab_size = vocab_size;
    model->d_model = d_model;
    model->num_blocks = num_blocks;
    model->max_len = max_len;

    // 1. Create Embedding Layer
    model->embedding_layer = embedding_layer_create(vocab_size, d_model);
    if (!model->embedding_layer) {
        fprintf(stderr, "Error: Failed to create embedding layer.\n");
        free(model);
        return NULL;
    }

    // 2. Create Positional Encoding Matrix
    model->positional_encoding = matrix_create_positional_encoding(max_len, d_model);
    if (!model->positional_encoding) {
        fprintf(stderr, "Error: Failed to create positional encoding matrix.\n");
        embedding_layer_destroy(model->embedding_layer);
        free(model);
        return NULL;
    }

    // 3. Create Transformer Blocks
    model->blocks = (TransformerBlock**)malloc(num_blocks * sizeof(TransformerBlock*));
    if (!model->blocks) {
        fprintf(stderr, "Error: Failed to allocate memory for Transformer blocks.\n");
        matrix_destroy(model->positional_encoding);
        embedding_layer_destroy(model->embedding_layer);
        free(model);
        return NULL;
    }

    for (int i = 0; i < num_blocks; i++) {
        model->blocks[i] = transformer_block_create(d_model, ffn_hidden_dim);
        if (!model->blocks[i]) {
            fprintf(stderr, "Error: Failed to create Transformer block %d.\n", i);
            // Cleanup previously created blocks
            for (int j = 0; j < i; j++) {
                transformer_block_destroy(model->blocks[j]);
            }
            free(model->blocks);
            matrix_destroy(model->positional_encoding);
            embedding_layer_destroy(model->embedding_layer);
            free(model);
            return NULL;
        }
    }

    return model;
}

void transformer_model_destroy(TransformerModel* model) {
    if (!model) return;

    embedding_layer_destroy(model->embedding_layer);
    matrix_destroy(model->positional_encoding);
    for (int i = 0; i < model->num_blocks; i++) {
        transformer_block_destroy(model->blocks[i]);
    }
    free(model->blocks);
    free(model);
}

Matrix* transformer_model_forward(const TransformerModel* model, const int* token_ids, int sequence_length) {
    // 1. Get token embeddings
    Matrix* embeddings = embedding_layer_forward(model->embedding_layer, token_ids, sequence_length);
    if (!embeddings) {
        fprintf(stderr, "Error: Embedding layer forward pass failed.\n");
        return NULL;
    }

    // 2. Add positional encoding
    // Note: This is a simplification. A more robust implementation would slice the PE matrix.
    // Here we assume sequence_length <= max_len.
    for(int i = 0; i < sequence_length; i++) {
        for(int j = 0; j < model->d_model; j++) {
            embeddings->data[i][j] += model->positional_encoding->data[i][j];
        }
    }

    // 3. Pass through Transformer Blocks
    Matrix* current_output = embeddings; // Start with the embeddings + PE
    Matrix* prev_output = NULL;

    for (int i = 0; i < model->num_blocks; i++) {
        prev_output = current_output;
        current_output = transformer_block_forward(model->blocks[i], prev_output);

        if(prev_output != embeddings) { // Avoid double-freeing the initial embeddings matrix
            matrix_destroy(prev_output);
        }

        if (!current_output) {
            fprintf(stderr, "Error: Forward pass failed at Transformer block %d.\n", i);
            matrix_destroy(embeddings);
            return NULL;
        }
    }

    // The initial embeddings matrix has been used and its content passed along, so we can destroy it.
    if(model->num_blocks > 0) matrix_destroy(embeddings);


    return current_output;
}
