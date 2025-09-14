use core::poseidon::PoseidonTrait;
use core::hash::HashStateTrait;


fn main (input: Array<felt252>) -> Array<felt252> {
    let user_address: felt252 = *input.at(0);

    let token: felt252 = *input.at(1);
    let token_hash: felt252 = PoseidonTrait::new().update(token).finalize();

    let tokens_hashes_len: felt252 = *input.at(2);
    
    let mut idx_last_token_hash: u32 = tokens_hashes_len.try_into().unwrap();
    idx_last_token_hash = idx_last_token_hash + 3_u32;

    let mut result = false;
    let mut output: Array<felt252> = ArrayTrait::new();
    output.append(user_address);
    output.append(token_hash);
    // output.append(token);
    // output.append(token_hash);

    let mut i = 3;
    while i != idx_last_token_hash {

        let val: felt252 = *input.at(i);
        if (token_hash == val){
            result = true;
        }
        i += 1;
        output.append(val);
    };


    assert!(result, "Token hash not included");
    // let mut output_serialized: Array<felt252> = ArrayTrait::new();
    // output.serialize(ref output_serialized);
    // output_serialized
    output
}