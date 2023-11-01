from fibonacccy.fibonacci_lists import FiboRustList


def test_list_fibo():
    list_fibonacci = FiboRustList()
    
    assert list_fibonacci.fibo_list(47)[46] == 1836311903