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

| Name       | 🐀 C-lang | 🦀 Rust  | 🐍 Python |
| ---------- | --------- | -------- | --------- |
| Min (ms)   | 4.0689    | 5.2180   | 508.6570  |
| Max (ms)   | 5.0728    | 5.7802   | 510.7501  |
| Mean (ms)  | 4.2315    | 5.2712   | 509.7133  |
| StdDev     | 0.1857    | 0.0752   | 0.8249    |
| Median     | 4.1928    | 5.2443   | 509.7957  |
| IQR        | 0.1157    | 0.0421   | 1.2900    |
| Outliers   | 27;28     | 19;20    | 2;0       |
| OPS        | 236.3224  | 189.7092 | 1.9619    |
| Rounds     | 233       | 169      | 5         |
| Iterations | 1         | 1        | 1         |

## LICENSE

- MIT License
