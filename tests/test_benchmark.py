from fibonacccy.fibonacci import fibo
import pytest
import time

def fibonacci_rust_benchmark():
    return fibo(30, "rust")

def fibonacci_clang_benchmark():
    return fibo(30, "clang")

def fibonacci_python_benchmark():
    return fibo(30, "python")

@pytest.mark.benchmark(group="fibonacci", timer=time.time)
def test_fibonacci_rust(benchmark):
    result = benchmark(fibonacci_rust_benchmark)

@pytest.mark.benchmark(group="fibonacci", timer=time.time)
def test_fibonacci_clang(benchmark):
    result = benchmark(fibonacci_clang_benchmark)

@pytest.mark.benchmark(group="fibonacci", timer=time.time)
def test_fibonacci_python(benchmark):
    result = benchmark(fibonacci_python_benchmark)
