import unittest
import sys
import os

# Add the parent directory to the path so we can import from python_interface
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_interface.carl import NeuralNetwork, Matrix

class TestPersistence(unittest.TestCase):

    def test_save_and_load(self):
        """
        Tests the full cycle of training, saving, loading, and predicting.
        """
        filepath = "test_model.ccia"
        topology = [2, 3, 1]

        # 1. Train a network
        nn_original = NeuralNetwork(topology)
        training_data = [{'input': [0.0, 1.0], 'target': [1.0]}] # Simple data is enough

        # Train for a few epochs to move weights away from random initialization
        for _ in range(100):
            input_matrix = Matrix.from_list([training_data[0]['input']])
            target_matrix = Matrix.from_list([training_data[0]['target']])
            nn_original.train(input_matrix, target_matrix, 0.1)

        # 2. Get original prediction and save
        original_prediction = nn_original.forward(Matrix.from_list([training_data[0]['input']])).to_list()[0][0]
        nn_original.save(filepath)

        # 3. Load the network into a new instance
        nn_loaded = NeuralNetwork.load(filepath)
        loaded_prediction = nn_loaded.forward(Matrix.from_list([training_data[0]['input']])).to_list()[0][0]

        # 4. Assert that the loaded network has the same state
        self.assertEqual(nn_original.topology, nn_loaded.topology, "La topología de la red cargada no coincide.")
        self.assertAlmostEqual(original_prediction, loaded_prediction, places=6,
                               msg="La predicción del modelo cargado es diferente a la del original.")

        # Clean up the created file
        os.remove(filepath)

if __name__ == '__main__':
    unittest.main()
