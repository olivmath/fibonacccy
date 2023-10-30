from ctypes import CDLL, c_uint, c_ulonglong


class FiboPython:
    """
    # Python class that use Rust fibonacci implementation
    """

    def __init__(self) -> None:
        ...

    def fibo(self, length: int) -> int:
        """
        # This function use `Pure Python` implementation under the hood
        """
        if length <= 1:
            return length

        return fibo(length - 1) + fibo(length - 2)


class FiboClang:
    """
    # Python class that use Clang fibonacci implementation
    """

    def __init__(self) -> None:
        path: str = "fibonacccy/clang_version/libfibonacccy_c.so"
        self.fibonacci_clang_lib = CDLL(path)
        self.fibonacci_clang_lib.fibo.argtypes = [c_uint]
        self.fibonacci_clang_lib.fibo.restype = c_ulonglong

    def fibo(self, length: int) -> int:
        """
        # This function use `Clang` implementation under the hood
        """
        return self.fibonacci_clang_lib.fibo(length)


class FiboRust:
    """
    # Python class that use Rust fibonacci implementation
    """

    def __init__(self):
        path: str = "fibonacccy/rust_version/libfibonacccy_rs.dylib"
        self.fibonacci_rust_lib = CDLL(path)
        self.fibonacci_rust_lib.fibo.argtypes = [c_uint]
        self.fibonacci_rust_lib.fibo.restype = c_ulonglong

    def fibo(self, length: int) -> int:
        """
        # This function use `Rust` implementation under the hood
        """
        return self.fibonacci_rust_lib.fibo(length)


def fibo(index: int, implementation="python") -> int:
    """
    Returns the index number of fibonacci sequence
    @param index: int
    @param implementation: "python" | "rust" | "clang"
    """

    if implementation == "python":
        return FiboPython().fibo(index)
    if implementation == "rust":
        return FiboRust().fibo(index)
    if implementation == "clang":
        return FiboClang().fibo(index)

    raise ValueError("Unknown implementation choice")
