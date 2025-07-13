use core::poseidon::PoseidonTrait;
use core::hash::{HashStateTrait, HashStateExTrait, };


fn send_vote()

fn main() -> felt252 {
    let ticket = Ticket { token: 123};
    let hash = PoseidonTrait::new().update_with(ticket).finalize();
    // println!(hash);
    hash
}