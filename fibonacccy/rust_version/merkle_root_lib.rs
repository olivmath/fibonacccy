use std::slice;

#[no_mangle]
pub extern "C" fn modify_mutable_array(ptr: *mut u8, len: usize) {
    let slice = unsafe { slice::from_raw_parts_mut(ptr, len) };
    slice.reverse();

}
