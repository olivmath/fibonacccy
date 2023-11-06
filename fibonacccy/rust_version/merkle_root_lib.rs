use std::slice;
use std::mem;

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
    let mut result_ptrs = Vec::with_capacity(len);

    for &inner_ptr in arrays {
        let inner_array = unsafe { slice::from_raw_parts(inner_ptr, 5) };
        let mut reversed_array = inner_array.to_vec();
        reversed_array.reverse();
        result_ptrs.push(reversed_array.into_boxed_slice());
    }

    let mut boxed_arrays: Vec<*mut u8> =
        result_ptrs.iter_mut().map(|arr| arr.as_mut_ptr()).collect();
    let ptr = boxed_arrays.as_mut_ptr();
    mem::forget(result_ptrs);
    mem::forget(boxed_arrays);

    ptr
}

#[no_mangle]
pub extern "C" fn free_array_of_arrays(ptr: *mut *mut u8, len: usize) {
    unsafe {
        let _ = Box::from_raw(slice::from_raw_parts_mut(ptr, len));
    }
}


// #[no_mangle]
// pub extern "C" fn reverse_immutable_array_of_arrays(
//     array_of_arrays_ptr: *const *const u8,
//     len: usize,
// ) -> *mut *mut u8 {
//     let arrays = unsafe { slice::from_raw_parts(array_of_arrays_ptr, len) };
//     let mut result_ptrs = Vec::with_capacity(len);

//     for &inner_ptr in arrays {
//         let inner_array = unsafe { slice::from_raw_parts(inner_ptr, 5) };
//         let mut reversed_array = inner_array.to_vec();
//         reversed_array.reverse();
//         let x = Box::into_raw(reversed_array.into_boxed_slice()) as *mut u8;
//         result_ptrs.push(x);
//     }

//     let boxed_ptrs = result_ptrs.into_boxed_slice();
//     let ptr_array = Box::into_raw(boxed_ptrs) as *mut *mut u8;

//     ptr_array
// }

// #[no_mangle]
// pub extern "C" fn free_array_of_arrays(ptr: *mut *mut u8, len: usize) {
//     unsafe {
//         let _ = Box::from_raw(slice::from_raw_parts_mut(ptr, len));
//     }
// }
