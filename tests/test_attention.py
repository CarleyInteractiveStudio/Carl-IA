import unittest
import sys
import os
import numpy as np

# Add the parent directory to the path so we can import from python_interface
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_interface.carl import Matrix, scaled_dot_product_attention

class TestAttention(unittest.TestCase):

    def test_attention_against_numpy(self):
        """
        Verifies the C implementation of scaled dot-product attention
        by comparing its output to a NumPy implementation.
        """
        seq_len, d_k, d_v = 4, 8, 10
        np.random.seed(42)
        q_data = np.random.rand(seq_len, d_k)
        k_data = np.random.rand(seq_len, d_k)
        v_data = np.random.rand(seq_len, d_v)

        # NumPy calculation
        def softmax(x):
            e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
            return e_x / e_x.sum(axis=-1, keepdims=True)

        scores = np.matmul(q_data, k_data.T)
        scaled_scores = scores / np.sqrt(d_k)
        attention_weights = softmax(scaled_scores)
        numpy_result = np.matmul(attention_weights, v_data)

        # Carl C library calculation
        q_carl = Matrix.from_list(q_data.tolist())
        k_carl = Matrix.from_list(k_data.tolist())
        v_carl = Matrix.from_list(v_data.tolist())
        carl_result_matrix = scaled_dot_product_attention(q_carl, k_carl, v_carl)
        carl_result = np.array(carl_result_matrix.to_list())

        # Assert that the results are almost equal
        self.assertTrue(np.allclose(numpy_result, carl_result, atol=1e-6),
                        "El resultado de la atención en C difiere significativamente del de NumPy.")

if __name__ == '__main__':
    unittest.main()
