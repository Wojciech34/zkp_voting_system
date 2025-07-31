use core::poseidon::PoseidonTrait;
// use core::poseidon::poseidon_hash_span;
use core::hash::HashStateTrait;
//use core::hash::{HashStateTrait, HashStateExTrait};


fn main (input: Array<felt252>) -> Array<felt252> {
    let token = *input.at(0);
    let token_hash = PoseidonTrait::new().update(token).finalize();
    // let x = poseidon_hash_span()

    let expected_hashes_len = *input.at(1);
    let mut expected_hashes_len: u32 = expected_hashes_len.try_into().unwrap();
    expected_hashes_len = expected_hashes_len + 2_u32;

    let mut result = false;

    let mut i = 2;
    while i != expected_hashes_len {
               
        let val = *input.at(i);
        if (token_hash == val){
            result = true;
        }
        i += 1;
    };

    // let mut result = false;
    // let hash = PoseidonTrait::new().update_with(pk).finalize();
    // if (hash == expected_hash){
    //     result = true;
    // }
    // assert!(result);
    let mut output: Array<felt252> = ArrayTrait::new();
    result.serialize(ref output);
    output
}