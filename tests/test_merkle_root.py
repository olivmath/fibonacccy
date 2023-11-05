from ctypes import CDLL, c_ubyte, c_size_t, POINTER


def test_reverse_mutable_array():
    lib = CDLL("fibonacccy/rust_version/libmerkle_root.dylib")
    lib.reverse_mutable_array.argtypes = (POINTER(c_ubyte), c_size_t)
    lib.reverse_mutable_array.restype = None

    data = b"lucas"
    array_type = c_ubyte * len(data)
    array_data = array_type(*data)

    lib.reverse_mutable_array(array_data, len(data))

    assert bytes(array_data) == b"sacul"


def test_reverse_immutable_array():
    lib = CDLL("fibonacccy/rust_version/libmerkle_root.dylib")
    lib.reverse_immutable_array.argtypes = (POINTER(c_ubyte), c_size_t)
    lib.reverse_immutable_array.restype = POINTER(c_ubyte)

    lib.free_immutable_array.argtypes = (POINTER(c_ubyte), c_size_t)
    lib.free_immutable_array.restype = None

    data = b"lucas"
    array_type = c_ubyte * len(data)
    array_data = array_type(*data)

    result_ptr = lib.reverse_immutable_array(array_data, len(data))
    result = bytes(result_ptr[: len(data)])
    lib.free_immutable_array(result_ptr, len(data))

    assert result == b"sacul"

