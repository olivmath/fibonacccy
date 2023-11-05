use std::slice;

#[no_mangle]
pub extern "C" fn reverse_mutable_array(ptr: *mut u8, len: usize) {
    let slice = unsafe { slice::from_raw_parts_mut(ptr, len) };
    slice.reverse();
}

#[no_mangle]
pub extern "C" fn reverse_immutable_array(ptr: *mut u8, len: usize) -> *mut u8 {
    let array = unsafe { slice::from_raw_parts(ptr, len) };
    let mut output_vec = array.to_vec();
    output_vec.reverse();

    let boxed_array = output_vec.into_boxed_slice();
    let ptr = Box::into_raw(boxed_array) as *mut u8;

    ptr
}

#[no_mangle]
pub extern "C" fn free_immutable_array(ptr: *mut u8, len: usize) {
    unsafe {
        let _ = Box::from_raw(slice::from_raw_parts_mut(ptr, len as usize));
    }
}
