from ctypes import CDLL, c_ubyte, c_size_t, POINTER


def test_modify_mutable_array():
    lib = CDLL("fibonacccy/rust_version/libmerkle_root.dylib")
    lib.modify_mutable_array.argtypes = (POINTER(c_ubyte), c_size_t)
    lib.modify_mutable_array.restype = None

    data = b"lucas"
    array_type = c_ubyte * len(data)
    array_data = array_type(*data)

    lib.modify_mutable_array(array_data, len(data))

    assert bytes(array_data) == b"sacul"
