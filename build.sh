gcc -shared -o fibonacccy/clang_version/libfibonacccy_c.so fibonacccy/clang_version/fibonacci.c
rustc --crate-type cdylib fibonacccy/rust_version/lib.rs -o fibonacccy/rust_version/libfibonacccy_rs.dylib
rustc --crate-type cdylib fibonacccy/rust_version/merkle_root_lib.rs -o fibonacccy/rust_version/libmerkle_root.dylib
