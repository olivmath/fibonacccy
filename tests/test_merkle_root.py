from ctypes import (
    CDLL,
    CFUNCTYPE,
    c_ubyte,
    c_size_t,
    POINTER,
    cast,
    memmove,
)
import hashlib
import pytest


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
    array_ptr = array_type(*data)

    result_ptr = lib.reverse_immutable_array(array_ptr, len(data))
    result = bytes(result_ptr[: len(data)])
    lib.free_immutable_array(result_ptr, len(data))

    assert result == b"sacul"


def test_reverse_immutable_array_of_arrays():
    lib = CDLL("fibonacccy/rust_version/libmerkle_root.dylib")
    lib.reverse_immutable_array_of_arrays.argtypes = (
        POINTER(POINTER(c_ubyte)),
        c_size_t,
    )
    lib.reverse_immutable_array_of_arrays.restype = POINTER(POINTER(c_ubyte))

    lib.free_array_of_arrays.argtypes = (POINTER(POINTER(c_ubyte)), c_size_t)
    lib.free_array_of_arrays.restype = None

    data = [b"lucas", b"grazy", b"elise"]

    pointer_array_type = POINTER(c_ubyte) * len(data)
    pointers = pointer_array_type(
        *[cast((c_ubyte * 5).from_buffer_copy(d), POINTER(c_ubyte)) for d in data]
    )

    result_ptrs = lib.reverse_immutable_array_of_arrays(pointers, len(data))

    result = [bytes(result_ptrs[i][:5]) for i in range(len(data))]
    lib.free_array_of_arrays(result_ptrs, len(data))

    assert len(result) == len(data)
    for i in result:
        assert len(i) == 5
    assert result == [b"sacul", b"yzarg", b"esile"]
    with pytest.raises(ValueError) as excinfo:
        result = [bytes(result_ptrs[i][:5]) for i in range(len(data))]
    assert "NULL pointer access" in str(excinfo.value)


def test_passing_function():
    callback_function = CFUNCTYPE(None, POINTER(c_ubyte), POINTER(c_ubyte))

    @callback_function
    def python_callback(ptr, output_ptr):
        data = bytes(ptr[:64])
        hashed = hashlib.sha256(data)
        memmove(output_ptr, hashed.digest(), 32)

    lib = CDLL("fibonacccy/rust_version/libmerkle_root.dylib")
    lib.exec_hash.argtypes = [callback_function, POINTER(c_ubyte)]
    lib.exec_hash.restype = POINTER(c_ubyte)
    lib.free_32.argtypes = [POINTER(c_ubyte)]
    lib.free_32.restype = None

    array_data = b"3ac225168df54212a25c1c01fd35bebfea408fdac2e31ddd6f80a4bbf9a5f1cb"
    array_type = c_ubyte * 64
    array_ptr = array_type(*array_data)

    result_ptr = lib.exec_hash(python_callback, array_ptr)

    result = bytes(result_ptr[:32])
    lib.free_32(result_ptr)

    assert result.hex() == "df1055e0d9a89743ba6d0331cd81ecca579d5ffa250c109c4f2070cfdff9dbc4"
    assert result == bytes.fromhex("df1055e0d9a89743ba6d0331cd81ecca579d5ffa250c109c4f2070cfdff9dbc4")


def test_passing_function_and_array_of_arrays():
    callback_function = CFUNCTYPE(None, POINTER(c_ubyte), POINTER(c_ubyte))

    @callback_function
    def python_callback(ptr, output_ptr):
        data = bytes(ptr[:64])
        hashed = hashlib.sha256(data)
        memmove(output_ptr, hashed.digest(), 32)

    lib = CDLL("fibonacccy/rust_version/libmerkle_root.dylib")
    lib.make_root.argtypes = (
        callback_function,
        POINTER(POINTER(c_ubyte)),
        c_size_t,
    )
    lib.make_root.restype = POINTER(c_ubyte)

    lib.free_32.argtypes = [POINTER(c_ubyte)]
    lib.free_32.restype = None

    leafs = [
        bytes.fromhex("3ac225168df54212a25c1c01fd35bebfea408fdac2e31ddd6f80a4bbf9a5f1cb"),
        bytes.fromhex("b5553de315e0edf504d9150af82dafa5c4667fa618ed0a6f19c69b41166c5510"),
        bytes.fromhex("0b42b6393c1f53060fe3ddbfcd7aadcca894465a5a438f69c87d790b2299b9b2"),
        bytes.fromhex("f1918e8562236eb17adc8502332f4c9c82bc14e19bfc0aa10ab674ff75b3d2f3"),
    ]
    pointer_array_type = POINTER(c_ubyte) * len(leafs)
    pointers = pointer_array_type(
        *[cast((c_ubyte * 32).from_buffer_copy(leaf), POINTER(c_ubyte)) for leaf in leafs]
    )

    result_ptr = lib.make_root(python_callback, pointers, len(leafs))
    result = bytes(result_ptr[:32])
    lib.free_32(result_ptr)

    expected = "709472e68a228e0904b196b31863598a1bb675d5c8bda458045a18cdb8804b7e"
    expected_bytes = bytes.fromhex(expected)
    assert result.hex() == expected
    assert result == expected_bytes
