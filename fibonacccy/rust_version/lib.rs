#[no_mangle]
pub extern "C" fn fibo_recursive(length: u32) -> u64 {
    if length <= 1 {
        return length as u64;
    }

    fibo(length - 1) + fibo(length - 2)
}

#[no_mangle]
pub extern "C" fn fibo_iter(length: u32) -> u64 {
    if length <= 1 {
        return length as u64;
    }

    let mut a = 0;
    let mut b = 1;
    let mut fib = 0;

    for _ in 2..=length {
        fib = a + b;
        a = b;
        b = fib;
    }

    fib as u64
}

#[no_mangle]
pub extern "C" fn fibo_matrix_exponential(n: u32) -> u64 {
    if n == 0 {
        return 0;
    }

    // Matriz de transformação
    let mut a = [[1, 1], [1, 0]];
    let mut result = [[1, 0], [0, 1]];

    let mut b = a;

    let mut m = n - 1;
    while m > 0 {
        if m % 2 == 1 {
            result = matrix_multiply(&result, &b);
        }
        b = matrix_multiply(&b, &b);
        m /= 2;
    }

    result[0][0] as u64
}

fn matrix_multiply(a: &[[u64; 2]; 2], b: &[[u64; 2]; 2]) -> [[u64; 2]; 2] {
    [
        [
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ],
        [
            a[1][0] * b[0][0] + a[1][1] * b[1][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ],
    ]
}

#[no_mangle]
pub extern "C" fn fibonacci(n: i32) -> *mut i32 {
    if n <= 0 {
        return std::ptr::null_mut();
    }

    let mut seq = Vec::with_capacity(n as usize);
    for i in 0..n {
        seq.push(fibo(i as u32) as i32);
    }

    let boxed_seq = seq.into_boxed_slice();
    let ptr = Box::into_raw(boxed_seq) as *mut i32;

    ptr
}

#[no_mangle]
pub extern "C" fn free_fib(ptr: *mut i32, n: i32) {
    unsafe {
        let _boxed = Box::from_raw(std::slice::from_raw_parts_mut(ptr, n as usize));
    }
}
