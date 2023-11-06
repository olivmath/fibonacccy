use std::slice;

#[no_mangle]
pub extern "C" fn reverse_mutable_array(ptr: *mut u8, len: usize) {
    let slice = unsafe { slice::from_raw_parts_mut(ptr, len) };
    slice.reverse();
}

#[no_mangle]
pub extern "C" fn reverse_immutable_array(ptr: *const u8, len: usize) -> *mut u8 {
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
        let _ = Box::from_raw(slice::from_raw_parts_mut(ptr, len));
    }
}
#[no_mangle]
pub extern "C" fn reverse_immutable_array_of_arrays(
    array_of_arrays_ptr: *const *const u8,
    len: usize,
) -> *mut *mut u8 {
    let arrays = unsafe { slice::from_raw_parts(array_of_arrays_ptr, len) };

    let result_ptrs: Vec<_> = arrays
        .iter()
        .map(|&inner_ptr| {
            let inner_array = unsafe { slice::from_raw_parts(inner_ptr, 5) };
            inner_array
                .iter()
                .rev()
                .cloned()
                .collect::<Vec<u8>>()
                .into_boxed_slice()
        })
        .map(|boxed_slice| Box::into_raw(boxed_slice) as *mut u8)
        .collect();

    let ptr_array = Box::into_raw(result_ptrs.into_boxed_slice()) as *mut *mut u8;

    ptr_array
}

#[no_mangle]
pub extern "C" fn free_array_of_arrays(ptr: *mut *mut u8, len: usize) {
    unsafe {
        let mut boxed_ptrs = Box::from_raw(slice::from_raw_parts_mut(ptr, len));
        boxed_ptrs.iter_mut().for_each(|&mut inner_ptr| {
            let _ = Box::from_raw(inner_ptr);
        });
    }
}
