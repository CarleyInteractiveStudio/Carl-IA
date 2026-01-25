import unittest
import sys
import os

# Add the parent directory to the path so we can import from python_interface
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_interface.carl import EmbeddingLayer
from python_interface.tokenizer import SimpleTokenizer

class TestEmbedding(unittest.TestCase):

    def test_embedding_forward_pass(self):
        """
        Tests the full workflow of tokenizing text and using the EmbeddingLayer.
        """
        # 1. Tokenizer setup
        tokenizer = SimpleTokenizer()
        sample_texts = ["carl es un modelo", "de lenguaje"]
        tokenizer.fit(sample_texts)

        test_sentence = "carl es de lenguaje"
        token_ids = tokenizer.tokenize(test_sentence)
        sequence_length = len(token_ids)

        # 2. EmbeddingLayer setup
        vocab_size = tokenizer.vocab_size
        embedding_dim = 16
        embedding_layer = EmbeddingLayer(vocab_size, embedding_dim)

        # 3. Forward pass
        output_matrix = embedding_layer.forward(token_ids)

        # 4. Assertions
        self.assertIsNotNone(output_matrix, "La salida de la capa de embedding no debería ser nula.")
        self.assertEqual(output_matrix.rows, sequence_length, "El número de filas de salida debe ser igual a la longitud de la secuencia.")
        self.assertEqual(output_matrix.cols, embedding_dim, "El número de columnas de salida debe ser igual a la dimensión del embedding.")

if __name__ == '__main__':
    unittest.main()
