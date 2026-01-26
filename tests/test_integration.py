import unittest
import sys
import os

# Add the parent directory to the path so we can import from python_interface
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_interface.carl import NeuralNetwork, Matrix

class TestIntegration(unittest.TestCase):

    def test_xor_forward_pass_runs(self):
        """
        Tests if a forward pass with XOR-like data completes without errors.
        This confirms that the Python wrapper and the C library are working together.
        """
        # Define the topology for the XOR problem
        topology = [2, 3, 1]

        try:
            nn = NeuralNetwork(topology)
        except Exception as e:
            self.fail(f"NeuralNetwork creation failed with an exception: {e}")

        # Define the XOR input data
        xor_inputs = [
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [1.0, 1.0]
        ]

        for input_data in xor_inputs:
            try:
                input_matrix = Matrix.from_list([input_data])
                output_matrix = nn.forward(input_matrix)
                # We just need to ensure it runs without crashing.
                self.assertIsNotNone(output_matrix)
                self.assertEqual(output_matrix.rows, 1)
                self.assertEqual(output_matrix.cols, 1)
            except Exception as e:
                self.fail(f"nn.forward() failed for input {input_data} with an exception: {e}")

if __name__ == '__main__':
    unittest.main()
