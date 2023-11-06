from ctypes import CDLL, c_ubyte, c_size_t, POINTER, cast
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
