from fibonacccy.fibonacci import fibo

def test_fibo_rust():
    result = fibo(10)
    assert result == 55, f"expected `10` return `{result}`"

def test_fibo_clang():
    result = fibo(10)
    assert result == 55, f"expected `10` return `{result}`"

def test_fibo_python():
    result = fibo(10)
    assert result == 55, f"expected `10` return `{result}`"
