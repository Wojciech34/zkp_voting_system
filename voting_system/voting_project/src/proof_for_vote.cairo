use core::poseidon::PoseidonTrait;
use core::hash::{HashStateTrait, HashStateExTrait};
// use integrity::{Integrity, IntegrityWithConfig, calculate_bootloaded_fact_hash, SHARP_BOOTLOADER_PROGRAM_HASH, VerifierConfiguration};


fn main (input: Array<felt252>) -> Array<felt252> {
    let pk = *input.at(0);
    let expected_hash = *input.at(1);
    let mut result = false;
    let hash = PoseidonTrait::new().update_with(pk).finalize();
    if hash == expected_hash{
        result = true;
    }
    // assert!(result);
    let mut output: Array<felt252> = ArrayTrait::new();
    result.serialize(ref output);
    output
}