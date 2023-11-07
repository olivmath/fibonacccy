use std::slice;

/// # Safety
///
/// essa funcao é um perigo menino
#[no_mangle]
pub unsafe extern "C" fn reverse_mutable_array(ptr: *mut u8, len: usize) {
    let slice = unsafe { slice::from_raw_parts_mut(ptr, len) };
    slice.reverse();
}

/// # Safety
///
/// essa funcao é um perigo menino
#[no_mangle]
pub unsafe extern "C" fn reverse_immutable_array(ptr: *const u8, len: usize) -> *mut u8 {
    let array = unsafe { slice::from_raw_parts(ptr, len) };
    let mut output_vec = array.to_vec();
    output_vec.reverse();

    let boxed_array = output_vec.into_boxed_slice();
    Box::into_raw(boxed_array) as *mut u8
}

/// # Safety
///
/// essa funcao é um perigo menino
#[no_mangle]
pub unsafe extern "C" fn free_immutable_array(ptr: *mut u8, len: usize) {
    unsafe {
        let _ = Box::from_raw(slice::from_raw_parts_mut(ptr, len));
    }
}

/// # Safety
///
/// essa funcao é um perigo menino
#[no_mangle]
pub unsafe extern "C" fn reverse_immutable_array_of_arrays(
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

    Box::into_raw(result_ptrs.into_boxed_slice()) as *mut *mut u8
}

/// # Safety
///
/// essa funcao é um perigo menino
#[no_mangle]
pub unsafe extern "C" fn free_array_of_arrays(ptr: *mut *mut u8, len: usize) {
    unsafe {
        let mut boxed_ptrs = Box::from_raw(slice::from_raw_parts_mut(ptr, len));
        boxed_ptrs.iter_mut().for_each(|&mut inner_ptr| {
            let _ = Box::from_raw(inner_ptr);
        });
    }
}

/// # Safety
///
/// essa funcao é um perigo menino
#[no_mangle]
pub unsafe extern "C" fn exec_hash(
    callback: extern "C" fn(input: *const u8, output: *mut u8),
    array_prt: *const u8,
) -> *mut u8 {
    let mut buffer: [u8; 32] = [0; 32];
    callback(array_prt, buffer.as_mut_ptr());

    let boxed_array = buffer.to_vec().into_boxed_slice();
    Box::into_raw(boxed_array) as *mut u8
}

/// # Safety
///
/// essa funcao é um perigo menino
#[no_mangle]
pub unsafe extern "C" fn free_32(ptr: *mut u8) {
    unsafe {
        let _ = Box::from_raw(slice::from_raw_parts_mut(ptr, 32));
    }
}

/// # Safety
///
/// essa funcao é um perigo menino
#[no_mangle]
pub unsafe extern "C" fn make_root(
    callback: extern "C" fn(input: *const u8, output: *mut u8),
    leafs_ptr: *const *const u8,
    len: usize,
) -> *mut u8 {
    let leafs = unsafe { slice::from_raw_parts(leafs_ptr, len) }
        .iter()
        .map(|&ptr| unsafe { Vec::from(slice::from_raw_parts(ptr, 32)) })
        .collect::<Vec<Vec<u8>>>();

    let mut nodes = leafs.clone();
    while nodes.len() > 1 {
        nodes = nodes
            .chunks(2)
            .map(|chunk| {
                let concat = if chunk.len() == 2 {
                    [chunk[0].as_slice(), chunk[1].as_slice()].concat()
                } else {
                    chunk[0].to_vec()
                };

                let mut buffer: [u8; 32] = [0; 32];
                callback(concat.as_ptr(), buffer.as_mut_ptr());

                buffer.to_vec()
            })
            .collect()
    }

    let root = nodes.into_iter().next().unwrap_or_default();
    println!("{:?}", root);
    let boxed_array = root.into_boxed_slice();
    Box::into_raw(boxed_array) as *mut u8
}
