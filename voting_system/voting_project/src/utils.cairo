#[derive(Drop, Hash)]
struct Ticket { // token allowing voting
    token: felt252,
}


#[derive(Drop)]
enum AllowedChoices {
    A,
    B,
    C,
}