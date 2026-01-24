#include "matrix.h"
#include <stdio.h>
#include <time.h>

// Helper function to allocate a 2D array for the matrix data
double** allocate_data(int rows, int cols) {
    double** data = (double**)malloc(rows * sizeof(double*));
    if (!data) return NULL;
    for (int i = 0; i < rows; i++) {
        data[i] = (double*)malloc(cols * sizeof(double));
        if (!data[i]) {
            // Clean up previously allocated rows on failure
            for (int j = 0; j < i; j++) {
                free(data[j]);
            }
            free(data);
            return NULL;
        }
    }
    return data;
}

Matrix* matrix_create(int rows, int cols) {
    Matrix* m = (Matrix*)malloc(sizeof(Matrix));
    if (!m) return NULL;
    m->rows = rows;
    m->cols = cols;
    m->data = allocate_data(rows, cols);
    if (!m->data) {
        free(m);
        return NULL;
    }
    return m;
}

void matrix_destroy(Matrix* m) {
    if (m == NULL) return;
    for (int i = 0; i < m->rows; i++) {
        free(m->data[i]);
    }
    free(m->data);
    free(m);
}

void matrix_randomize(Matrix* m) {
    // Seed the random number generator only once
    static int seeded = 0;
    if (!seeded) {
        srand(time(NULL));
        seeded = 1;
    }

    for (int i = 0; i < m->rows; i++) {
        for (int j = 0; j < m->cols; j++) {
            // Generate random double between -1.0 and 1.0
            m->data[i][j] = ((double)rand() / (double)RAND_MAX) * 2.0 - 1.0;
        }
    }
}

Matrix* matrix_copy(const Matrix* src) {
    if (!src) return NULL;
    Matrix* dst = matrix_create(src->rows, src->cols);
    if (!dst) return NULL;

    for (int i = 0; i < src->rows; i++) {
        for (int j = 0; j < src->cols; j++) {
            dst->data[i][j] = src->data[i][j];
        }
    }
    return dst;
}

void matrix_print(const Matrix* m) {
    if (m == NULL) {
        printf("Matrix is NULL.\n");
        return;
    }
    printf("Matrix (%d rows, %d cols):\n", m->rows, m->cols);
    for (int i = 0; i < m->rows; i++) {
        for (int j = 0; j < m->cols; j++) {
            printf("%10.4f ", m->data[i][j]);
        }
        printf("\n");
    }
}

Matrix* matrix_multiply(const Matrix* a, const Matrix* b) {
    if (a->cols != b->rows) {
        fprintf(stderr, "Error: Matrix multiplication dimensions are incompatible.\n");
        return NULL;
    }

    Matrix* result = matrix_create(a->rows, b->cols);
    if (!result) return NULL;

    for (int i = 0; i < result->rows; i++) {
        for (int j = 0; j < result->cols; j++) {
            double sum = 0;
            for (int k = 0; k < a->cols; k++) {
                sum += a->data[i][k] * b->data[k][j];
            }
            result->data[i][j] = sum;
        }
    }
    return result;
}

void matrix_add_bias(Matrix* m, const Matrix* bias) {
    if (m->cols != bias->cols || bias->rows != 1) {
        fprintf(stderr, "Error: Bias dimensions are incompatible for addition.\n");
        return;
    }

    for (int i = 0; i < m->rows; i++) {
        for (int j = 0; j < m->cols; j++) {
            m->data[i][j] += bias->data[0][j];
        }
    }
}

void matrix_map(Matrix* m, double (*func)(double)) {
    for (int i = 0; i < m->rows; i++) {
        for (int j = 0; j < m->cols; j++) {
            m->data[i][j] = func(m->data[i][j]);
        }
    }
}
