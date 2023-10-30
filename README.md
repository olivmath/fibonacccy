# Fibonacccy

## How It Works

This is a Proof of Concept (PoC) to test the feasibility of using other languages as an optimization alternative.

This project offers three implementations to calculate the nth number in the Fibonacci sequence, made in:

- Pure Python
- Rust
- C/C++ (Clang).

## Implementations

**Python**

```python
def fibo(self, length: int) -> int:
    if length <= 1:
        return length

    return fibo(length - 1) + fibo(length - 2)
```

**Rust**

```rust
#[no_mangle]
pub extern "C" fn fibo(length: u32) -> u64 {
    if length <= 1 {
        return length as u64;
    }

    fibo(length - 1) + fibo(length - 2)
}
```

**Clang**

```c
int fibo(int length) {
    if (length <= 1) {
        return length;
    }

    return fibo(length - 1) + fibo(length - 2);
}
```

## How to use

```python
from fibonacccy.fibonacci import fibo

# Calculate the 10th number in the Fibonacci sequence
result = fibo(10)  # implementation="python" DEFAULT
result = fibo(10, implementation="clang")
result = fibo(10, implementation="rust")
```

## Performance Benchmark

| Benchmark Name        | Min (ms) | Max (ms) | Mean (ms) | StdDev | Median   | IQR    | Outliers | OPS      | Rounds | Iterations |
| --------------------- | -------- | -------- | --------- | ------ | -------- | ------ | -------- | -------- | ------ | ---------- |
| test_fibonacci_clang  | 4.0689   | 5.0728   | 4.2315    | 0.1857 | 4.1928   | 0.1157 | 27;28    | 236.3224 | 233    | 1          |
| test_fibonacci_rust   | 5.2180   | 5.7802   | 5.2712    | 0.0752 | 5.2443   | 0.0421 | 19;20    | 189.7092 | 169    | 1          |
| test_fibonacci_python | 508.6570 | 510.7501 | 509.7133  | 0.8249 | 509.7957 | 1.2900 | 2;0      | 1.9619   | 5      | 1          |

## LICENSE

- MIT License
