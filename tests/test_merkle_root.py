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
        bytes.fromhex("ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"),
        bytes.fromhex("3e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d"),
        bytes.fromhex("2e7d2c03a9507ae265ecf5b5356885a53393a2029d241394997265a1a25aefc6"),
        bytes.fromhex("18ac3e7343f016890c510e93f935261169d9e3f565436429830faf0934f4f8e4"),
    ]
    pointer_array_type = POINTER(c_ubyte) * len(leafs)
    pointers = pointer_array_type(
        *[cast((c_ubyte * 32).from_buffer_copy(leaf), POINTER(c_ubyte)) for leaf in leafs]
    )

    result_ptr = lib.make_root(python_callback, pointers, len(leafs))
    result = bytes(result_ptr[:32])
    print(result)
    lib.free_32(result_ptr)
    print(result)

    expected = "14ede5e8e97ad9372327728f5099b95604a39593cac3bd38a343ad76205213e7"
    expected_bytes = bytes.fromhex(expected)
    assert result.hex() == expected +1
    assert result == expected_bytes
