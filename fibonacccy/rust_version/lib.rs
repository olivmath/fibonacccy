#[no_mangle]
pub extern "C" fn fibo(length: u32) -> u64 {
    if length <= 1 {
        return length as u64;
    }

    fibo(length - 1) + fibo(length - 2)
}
