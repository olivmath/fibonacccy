from ctypes import CDLL, POINTER, addressof, c_int32, c_uint


class FiboRustList:
    """
    Python class that uses the Rust Fibonacci implementation
    """

    def __init__(self):
        path: str = "fibonacccy/rust_version/libfibonacccy_rs.dylib"
        self.fibonacci_rust_lib = CDLL(path)

        self.fibonacci_rust_lib.fibonacci.argtypes = [c_uint]
        self.fibonacci_rust_lib.fibonacci.restype = POINTER(c_int32)

        self.fibonacci_rust_lib.free_fib.argtypes = [
            POINTER(c_int32),
            c_int32,
        ]
        self.fibonacci_rust_lib.free_fib.restype = None

    def fibo_list(self, length: int) -> list[int]:
        """
        This function uses the Rust implementation under the hood.
        """
        ptr = self.fibonacci_rust_lib.fibonacci(length)

        sequence = (c_int32 * length).from_address(addressof(ptr.contents))

        result = list(sequence)

        self.fibonacci_rust_lib.free_fib(ptr, length)

        return result
