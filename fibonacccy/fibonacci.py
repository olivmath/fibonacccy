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

    def fibo_iter(self, n):
        if n <= 1:
            return n

        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b

        return b

    def matrix_multiply(self, a, b):
        x = a[0][0] * b[0][0] + a[0][1] * b[1][0]
        y = a[0][0] * b[0][1] + a[0][1] * b[1][1]
        z = a[1][0] * b[0][0] + a[1][1] * b[1][0]
        w = a[1][0] * b[0][1] + a[1][1] * b[1][1]

        return [[x, y], [z, w]]

    def fibo_matrix_exponential(self, n):
        if n == 0:
            return 0

        a = [[1, 1], [1, 0]]
        result = [[1, 0], [0, 1]]

        m = n - 1
        while m > 0:
            if m % 2 == 1:
                result = self.matrix_multiply(result, a)
            a = self.matrix_multiply(a, a)
            m //= 2

        return result[0][0]


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
