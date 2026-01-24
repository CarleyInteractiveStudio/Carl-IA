import ctypes
import os

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

class CNeuralNetwork(ctypes.Structure):
    # Opaque structure for now, we only need the pointer
    pass

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
carl_lib.nn_create.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
carl_lib.nn_create.restype = ctypes.POINTER(CNeuralNetwork)

carl_lib.nn_destroy.argtypes = [ctypes.POINTER(CNeuralNetwork)]
carl_lib.nn_destroy.restype = None

carl_lib.nn_forward.argtypes = [ctypes.POINTER(CNeuralNetwork), ctypes.POINTER(CMatrix)]
carl_lib.nn_forward.restype = ctypes.POINTER(CMatrix)

carl_lib.nn_print.argtypes = [ctypes.POINTER(CNeuralNetwork)]
carl_lib.nn_print.restype = None


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
    def __init__(self, topology):
        self.topology = topology
        num_layers = len(topology)
        c_topology = (ctypes.c_int * num_layers)(*topology)
        self.ptr = carl_lib.nn_create(c_topology, num_layers)

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

    def __str__(self):
        carl_lib.nn_print(self.ptr)
        return f"<NeuralNetwork at {hex(id(self))}>"
