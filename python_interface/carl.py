import ctypes
import os
from enum import IntEnum

# Enum for activation functions, must match the C enum
class ActivationType(IntEnum):
    SIGMOID = 0
    RELU = 1

# --- Load the C library ---
# Construct the path to the shared library file
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib', 'libcarl_core.so'))
try:
    carl_lib = ctypes.CDLL(lib_path)
except OSError as e:
    print(f"Error loading C library from {lib_path}: {e}")
    print("Please ensure you have compiled the C code using 'make'.")
    exit(1)

# --- Define C Structures for ctypes ---
class CMatrix(ctypes.Structure):
    _fields_ = [("rows", ctypes.c_int),
                ("cols", ctypes.c_int),
                ("data", ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))]

class CLayer(ctypes.Structure):
    # Dummy definition, we only need the pointer type
    pass

class CNeuralNetwork(ctypes.Structure):
    _fields_ = [("num_layers", ctypes.c_int),
                ("topology", ctypes.POINTER(ctypes.c_int)),
                ("layers", ctypes.POINTER(CLayer))]

class CEmbeddingLayer(ctypes.Structure):
    _fields_ = [("embeddings", ctypes.POINTER(CMatrix))]

# --- Define Argument and Return Types for C Functions ---
# Matrix functions
carl_lib.matrix_create.argtypes = [ctypes.c_int, ctypes.c_int]
carl_lib.matrix_create.restype = ctypes.POINTER(CMatrix)

carl_lib.matrix_destroy.argtypes = [ctypes.POINTER(CMatrix)]
carl_lib.matrix_destroy.restype = None

carl_lib.matrix_print.argtypes = [ctypes.POINTER(CMatrix)]
carl_lib.matrix_print.restype = None

carl_lib.matrix_multiply.argtypes = [ctypes.POINTER(CMatrix), ctypes.POINTER(CMatrix)]
carl_lib.matrix_multiply.restype = ctypes.POINTER(CMatrix)


# Neural Network functions
carl_lib.nn_create.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
carl_lib.nn_create.restype = ctypes.POINTER(CNeuralNetwork)

carl_lib.nn_destroy.argtypes = [ctypes.POINTER(CNeuralNetwork)]
carl_lib.nn_destroy.restype = None

carl_lib.nn_forward.argtypes = [ctypes.POINTER(CNeuralNetwork), ctypes.POINTER(CMatrix)]
carl_lib.nn_forward.restype = ctypes.POINTER(CMatrix)

carl_lib.nn_print.argtypes = [ctypes.POINTER(CNeuralNetwork)]
carl_lib.nn_print.restype = None

carl_lib.nn_train.argtypes = [ctypes.POINTER(CNeuralNetwork), ctypes.POINTER(CMatrix), ctypes.POINTER(CMatrix), ctypes.c_double]
carl_lib.nn_train.restype = None

carl_lib.nn_save.argtypes = [ctypes.POINTER(CNeuralNetwork), ctypes.c_char_p]
carl_lib.nn_save.restype = None

carl_lib.nn_load.argtypes = [ctypes.c_char_p]
carl_lib.nn_load.restype = ctypes.POINTER(CNeuralNetwork)

carl_lib.nn_get_layer_activation.argtypes = [ctypes.POINTER(CNeuralNetwork), ctypes.c_int]
carl_lib.nn_get_layer_activation.restype = ctypes.c_int # Corresponds to the enum

# Embedding Layer functions
carl_lib.embedding_layer_create.argtypes = [ctypes.c_int, ctypes.c_int]
carl_lib.embedding_layer_create.restype = ctypes.POINTER(CEmbeddingLayer)

carl_lib.embedding_layer_destroy.argtypes = [ctypes.POINTER(CEmbeddingLayer)]
carl_lib.embedding_layer_destroy.restype = None

carl_lib.embedding_layer_forward.argtypes = [ctypes.POINTER(CEmbeddingLayer), ctypes.POINTER(ctypes.c_int), ctypes.c_int]
carl_lib.embedding_layer_forward.restype = ctypes.POINTER(CMatrix)


# --- Python Wrapper Classes ---

class Matrix:
    """A Python wrapper for the C Matrix structure."""
    def __init__(self, rows, cols, _ptr=None):
        if _ptr:
            self.ptr = _ptr
        else:
            self.ptr = carl_lib.matrix_create(rows, cols)

        self.rows = self.ptr.contents.rows
        self.cols = self.ptr.contents.cols

    def __del__(self):
        # The ctypes object might be gone before this is called
        if hasattr(self, 'ptr') and self.ptr and carl_lib:
            carl_lib.matrix_destroy(self.ptr)

    def __str__(self):
        # A bit of a hack to capture C's stdout, but good for debugging
        # Note: This is complex; a simpler way is to write a C function that returns a string.
        # For now, we'll just print directly from C.
        carl_lib.matrix_print(self.ptr)
        return f"<Matrix at {hex(id(self))}>"

    @classmethod
    def from_list(cls, data):
        """Creates a matrix from a list of lists."""
        rows = len(data)
        cols = len(data[0])
        mat = cls(rows, cols)
        for i in range(rows):
            for j in range(cols):
                mat.ptr.contents.data[i][j] = data[i][j]
        return mat

    def to_list(self):
        """Converts the matrix to a list of lists."""
        data = []
        for i in range(self.rows):
            row = [self.ptr.contents.data[i][j] for j in range(self.cols)]
            data.append(row)
        return data


class NeuralNetwork:
    """A Python wrapper for the C NeuralNetwork structure."""
    def __init__(self, topology, activations=None):
        self.topology = topology
        num_layers = len(topology)
        c_topology = (ctypes.c_int * num_layers)(*topology)

        c_activations = None
        if activations:
            if len(activations) != num_layers - 1:
                raise ValueError("The number of activations must match the number of layers minus one.")
            # We have num_layers - 1 layers with activations
            num_activations = len(activations)
            c_activations = (ctypes.c_int * num_activations)(*[act.value for act in activations])

        self.ptr = carl_lib.nn_create(c_topology, num_layers, c_activations)

    def __del__(self):
        if hasattr(self, 'ptr') and self.ptr and carl_lib:
            carl_lib.nn_destroy(self.ptr)

    def forward(self, input_data):
        """Performs a forward pass through the network."""
        if not isinstance(input_data, Matrix):
            raise TypeError("Input data must be a Matrix object.")

        result_ptr = carl_lib.nn_forward(self.ptr, input_data.ptr)
        if not result_ptr:
            raise Exception("Forward propagation failed in C.")

        return Matrix(rows=0, cols=0, _ptr=result_ptr)

    def train(self, input_data, target_data, learning_rate):
        """Performs a single training step."""
        if not isinstance(input_data, Matrix) or not isinstance(target_data, Matrix):
            raise TypeError("Input and target data must be Matrix objects.")

        carl_lib.nn_train(self.ptr, input_data.ptr, target_data.ptr, learning_rate)

    def __str__(self):
        carl_lib.nn_print(self.ptr)
        return f"<NeuralNetwork at {hex(id(self))}>"

    def save(self, filepath):
        """Saves the neural network to a file."""
        # Convert Python string to bytes for C
        c_filepath = filepath.encode('utf-8')
        carl_lib.nn_save(self.ptr, c_filepath)

    @classmethod
    def load(cls, filepath):
        """Loads a neural network from a file."""
        c_filepath = filepath.encode('utf-8')
        nn_ptr = carl_lib.nn_load(c_filepath)
        if not nn_ptr:
            raise Exception(f"Failed to load neural network from {filepath}")

        # We need to find the topology to create the Python object correctly.
        # This is a bit of a workaround as the C struct is opaque to Python.
        # We'll read it directly from the C pointer. A better way would be
        # to have a C function `nn_get_topology`.
        num_layers = nn_ptr.contents.num_layers
        topology = [nn_ptr.contents.topology[i] for i in range(num_layers)]

        # Create a new Python NeuralNetwork instance without calling nn_create again
        new_nn = cls.__new__(cls)
        new_nn.topology = topology
        new_nn.ptr = nn_ptr
        return new_nn

    def get_layer_activation(self, layer_index):
        """Gets the activation function type for a specific layer."""
        if not 0 <= layer_index < len(self.topology) - 1:
            raise IndexError("Layer index is out of bounds.")

        act_enum_val = carl_lib.nn_get_layer_activation(self.ptr, layer_index)
        return ActivationType(act_enum_val)

class EmbeddingLayer:
    """A Python wrapper for the C EmbeddingLayer structure."""
    def __init__(self, vocab_size, embedding_dim):
        self.ptr = carl_lib.embedding_layer_create(vocab_size, embedding_dim)
        if not self.ptr:
            raise MemoryError("Failed to create EmbeddingLayer in C.")

    def __del__(self):
        if hasattr(self, 'ptr') and self.ptr and carl_lib:
            carl_lib.embedding_layer_destroy(self.ptr)

    def forward(self, token_ids):
        """Performs a forward pass, converting token IDs to vectors."""
        if not isinstance(token_ids, list):
            raise TypeError("Input token_ids must be a list of integers.")

        sequence_length = len(token_ids)
        c_token_ids = (ctypes.c_int * sequence_length)(*token_ids)

        result_ptr = carl_lib.embedding_layer_forward(self.ptr, c_token_ids, sequence_length)
        if not result_ptr:
            raise Exception("EmbeddingLayer forward pass failed in C.")

        # Wrap the returned CMatrix pointer in a Python Matrix object
        return Matrix(rows=0, cols=0, _ptr=result_ptr)
