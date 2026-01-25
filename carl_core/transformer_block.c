#include <stdio.h>
#include <stdlib.h>
#include "transformer_block.h"
#include "attention.h"
#include "matrix.h" // For matrix_add

// Helper function to create the feed-forward network for the block
static NeuralNetwork* create_ffn(int input_dim, int hidden_dim) {
    // Topology: input -> hidden -> output (same as input)
    int topology[] = {input_dim, hidden_dim, input_dim};
    // Use ReLU for the hidden layer and no activation for the output (or linear)
    // We'll handle the "no activation" by simply not applying one in the forward pass logic if needed.
    // For now, we define the activations for the layers that exist.
    int activations[] = {RELU, SIGMOID}; // Placeholder for the second activation
    return nn_create(topology, 3, activations);
}

TransformerBlock* transformer_block_create(int input_dim, int ffn_hidden_dim) {
    TransformerBlock* block = (TransformerBlock*)malloc(sizeof(TransformerBlock));
    if (!block) {
        fprintf(stderr, "Error: Failed to allocate memory for TransformerBlock.\n");
        return NULL;
    }

    // Create weight matrices for Q, K, V
    block->Wq = matrix_create(input_dim, input_dim);
    block->Wk = matrix_create(input_dim, input_dim);
    block->Wv = matrix_create(input_dim, input_dim);

    if (!block->Wq || !block->Wk || !block->Wv) {
        fprintf(stderr, "Error: Failed to allocate memory for Q, K, V matrices.\n");
        matrix_destroy(block->Wq);
        matrix_destroy(block->Wk);
        matrix_destroy(block->Wv);
        free(block);
        return NULL;
    }

    // Randomize weights
    matrix_randomize(block->Wq);
    matrix_randomize(block->Wk);
    matrix_randomize(block->Wv);

    // Create the feed-forward network
    block->ffn = create_ffn(input_dim, ffn_hidden_dim);
    if (!block->ffn) {
        fprintf(stderr, "Error: Failed to create the feed-forward network for the block.\n");
        matrix_destroy(block->Wq);
        matrix_destroy(block->Wk);
        matrix_destroy(block->Wv);
        free(block);
        return NULL;
    }

    return block;
}

void transformer_block_destroy(TransformerBlock* block) {
    if (!block) return;

    matrix_destroy(block->Wq);
    matrix_destroy(block->Wk);
    matrix_destroy(block->Wv);
    nn_destroy(block->ffn);
    free(block);
}

Matrix* transformer_block_forward(const TransformerBlock* block, const Matrix* input) {
    // 1. Calculate Q, K, V matrices
    Matrix* Q = matrix_multiply(input, block->Wq);
    Matrix* K = matrix_multiply(input, block->Wk);
    Matrix* V = matrix_multiply(input, block->Wv);

    if (!Q || !K || !V) {
        fprintf(stderr, "Error: Matrix multiplication for Q, K, or V failed.\n");
        matrix_destroy(Q);
        matrix_destroy(K);
        matrix_destroy(V);
        return NULL;
    }

    // 2. Calculate Scaled Dot-Product Attention
    Matrix* attention_output = scaled_dot_product_attention(Q, K, V);
    if (!attention_output) {
         fprintf(stderr, "Error: Scaled dot-product attention failed.\n");
         matrix_destroy(Q);
         matrix_destroy(K);
         matrix_destroy(V);
         return NULL;
    }


    // 3. Add & Norm (Residual Connection 1)
    // For now, we only add. Normalization can be added later.
    Matrix* add_norm_1 = matrix_add(input, attention_output);
     if (!add_norm_1) {
         fprintf(stderr, "Error: First residual connection (matrix_add) failed.\n");
         matrix_destroy(Q);
         matrix_destroy(K);
         matrix_destroy(V);
         matrix_destroy(attention_output);
         return NULL;
    }

    // 4. Feed-Forward Network
    Matrix* ffn_output = nn_forward(block->ffn, add_norm_1);
     if (!ffn_output) {
         fprintf(stderr, "Error: Feed-forward network pass failed.\n");
         matrix_destroy(Q);
         matrix_destroy(K);
         matrix_destroy(V);
         matrix_destroy(attention_output);
         matrix_destroy(add_norm_1);
         return NULL;
    }

    // 5. Add & Norm (Residual Connection 2)
    Matrix* add_norm_2 = matrix_add(add_norm_1, ffn_output);
    if (!add_norm_2) {
         fprintf(stderr, "Error: Second residual connection (matrix_add) failed.\n");
         matrix_destroy(Q);
         matrix_destroy(K);
         matrix_destroy(V);
         matrix_destroy(attention_output);
         matrix_destroy(add_norm_1);
         matrix_destroy(ffn_output);
         return NULL;
    }


    // Cleanup intermediate matrices
    matrix_destroy(Q);
    matrix_destroy(K);
    matrix_destroy(V);
    matrix_destroy(attention_output);
    matrix_destroy(add_norm_1);
    matrix_destroy(ffn_output);

    return add_norm_2;
}
