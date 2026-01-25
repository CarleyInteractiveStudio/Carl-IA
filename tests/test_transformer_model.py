import unittest
import sys
import os

# Add the python_interface directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python_interface')))

from carl import TransformerModel, Matrix

class TestTransformerModel(unittest.TestCase):

    def test_forward_pass(self):
        """
        Tests a full forward pass through the Transformer model to ensure
        all components are connected and there are no runtime errors.
        """
        # Hyperparameters for a small test model
        vocab_size = 100
        d_model = 16
        num_blocks = 2
        max_len = 50
        ffn_hidden_dim = 32

        # Input sequence
        sequence_length = 5
        token_ids = [10, 2, 45, 99, 5]

        # 1. Create the model
        model = None
        try:
            model = TransformerModel(
                vocab_size=vocab_size,
                d_model=d_model,
                num_blocks=num_blocks,
                max_len=max_len,
                ffn_hidden_dim=ffn_hidden_dim
            )
            self.assertIsNotNone(model, "Model creation should not fail.")
            self.assertIsNotNone(model.ptr, "Model pointer should not be null.")

            # 2. Perform a forward pass
            output_matrix = model.forward(token_ids)
            self.assertIsInstance(output_matrix, Matrix, "Forward pass should return a Matrix object.")

            # 3. Check output dimensions
            self.assertEqual(output_matrix.rows, sequence_length, "Output matrix should have rows equal to sequence length.")
            self.assertEqual(output_matrix.cols, d_model, "Output matrix should have columns equal to d_model.")

            # 4. Check that output data is accessible (simple sanity check)
            output_list = output_matrix.to_list()
            self.assertEqual(len(output_list), sequence_length)
            self.assertEqual(len(output_list[0]), d_model)

        finally:
            # The __del__ method in the wrapper will handle cleanup
            if model:
                del model

if __name__ == '__main__':
    unittest.main()
