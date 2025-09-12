#[starknet::interface]
trait VoteTrait<T> {
    
    fn get_vote_status(self: @T) -> (u32, u32, u32, u32);

    fn vote(ref self: T, token_hash: felt252, vote: u8);

    fn add_tokens_hashes(ref self: T, tokens_hashes: Array<felt252>);

    fn get_all_tokens_hashes(self: @T) -> Array<felt252>;

    // fn test123(ref self: T, items: Array<felt252>) -> felt252;
    
}

#[starknet::contract]
mod Vote {

use core::poseidon::PoseidonTrait;
    use core::hash::HashStateTrait;
    use starknet::ContractAddress;
    use starknet::{get_caller_address};
    use starknet::storage::{
        StoragePointerReadAccess, StoragePointerWriteAccess, StorageMapReadAccess,
        StorageMapWriteAccess, Map
    };
    use integrity::{Integrity, IntegrityWithConfig, calculate_fact_hash};
    const YES: u8 = 1_u8;
    const NO: u8 = 0_u8;

    #[storage]
    struct Storage {
        yes_votes: u32,
        no_votes: u32,
        vote_ticket_number: u32,
        // dict storing users who voted
        users_who_voted: Map::<ContractAddress, bool>,
        // dict storing used hashed tokens
        used_tokens_hashes: Map::<felt252, bool>,
        admin_address: ContractAddress,
        hashed_tokens: Map::<u32, felt252>,
        hashed_tokens_number: u32,
    }

    #[constructor]
    fn constructor(
        ref self: ContractState,
    ) {
        self.yes_votes.write(0_u32);
        self.no_votes.write(0_u32);
        self.vote_ticket_number.write(0_u32);

        self.admin_address.write(get_caller_address());
        self.hashed_tokens_number.write(0_u32);

    }

    #[event]
    #[derive(Drop, starknet::Event)]
    enum Event {
        VoteCast: VoteCast,
        UnauthorizedAttempt: UnauthorizedAttempt,
        FactHash: FactHash,
        Output: Output
    }

    #[derive(Drop, starknet::Event)]
    struct VoteCast {
        voter: ContractAddress,
        vote: u8,
    }

    #[derive(Drop, starknet::Event)]
    struct UnauthorizedAttempt {
        unauthorized_address: ContractAddress,
    }

    #[derive(Drop, starknet::Event)]
    struct FactHash {
        fact_hash: felt252,
    }

    #[derive(Drop, starknet::Event)]
    struct Output {
        output: Span<felt252>,
    }

    // #[derive(Drop)]
    // struct VoteTicket {
    //     voter: ContractAddress,
    //     ticket_number: u8,
    // }

    #[abi(embed_v0)]
    impl VoteImpl of super::VoteTrait<ContractState> {
        // data returned is in hexadecimal format
        fn get_vote_status(self: @ContractState) -> (u32, u32, u32, u32) {
            let (n_yes, n_no) = self._get_voting_result();
            let (yes_percentage, no_percentage) = self._get_voting_result_in_percentage();
            (n_yes, n_no, yes_percentage, no_percentage)
        }

        // fn test123(ref self: ContractState, items: Array<felt252>) -> felt252 {
        //     let mut output_hash = PoseidonTrait::new();
        //     let new_items = items.span();

        //     self.emit(Output {output: new_items});

        //     for el in new_items {
        //         output_hash = output_hash.update(*el);
        //         self.emit(FactHash {fact_hash: *el});
        //     };
        //     let m = output_hash.finalize();
        //     self.emit(FactHash {fact_hash: m});
        //     // output_hash.finalize()
        //     m
            
        // }

        fn vote(ref self: ContractState, token_hash:felt252, vote: u8) {
            assert!(vote == NO || vote == YES, "Vote_0_OR_1");
            let caller: ContractAddress = get_caller_address();
            

            // ********************************************************
            // check that caller address and his token wasnt used in voting
            // ********************************************************

            self._assert_user_not_voted(caller);
            self._assert_token_hash_not_used(token_hash);
            
            let caller_felt252 : felt252 = caller.into();

            // ********************************************************
            // verify that proof for caller address has been registered
            // ********************************************************


            // required security bits
            let SECURITY_BITS = 32;

            // hash of a program, from which proof should be generated
            let program_hash = 0x42b84f0d9d23d1c67a0271f4e6577b1715214c88f8e7912abb92e6daa4ff58a;
            
            // expected output of a program, which is [caller address, user_hashed_token, hashed_token1, hashed_token2 ... hashed_tokenN]
            let tokens_hashes = self._get_all_tokens_hashes().span();
            let mut expected_output: Array<felt252> = ArrayTrait::new();

            // output in proof slightly differs because of the way cairo-vm adds output
            expected_output.append(0);

            let hashed_tokens_number_felt252: felt252 = self.hashed_tokens_number.read().into();
            expected_output.append(hashed_tokens_number_felt252 + 2);            
            expected_output.append(caller_felt252);
            expected_output.append(token_hash);
            
            for token_hash in tokens_hashes {
                expected_output.append(*token_hash);
            };
        

            let expected_output_span = expected_output.span();

            // with program hash and otput fact_hash can be calculated
            let fact_hash = calculate_fact_hash(program_hash, expected_output_span);

            let integrity = Integrity::new();
            // check if fact_hash was registered
            let mut is_verified = false;
            if integrity.is_fact_hash_valid_with_security(fact_hash, SECURITY_BITS) {
                is_verified = true;
            }

            assert!(is_verified, "Account with this address did not register valid fact hash of possesing token");
            

            self.users_who_voted.write(caller, true);
            self.used_tokens_hashes.write(token_hash, true);

            if (vote == NO) {
                self.no_votes.write(self.no_votes.read() + 1_u32);
            }
            if (vote == YES) {
                self.yes_votes.write(self.yes_votes.read() + 1_u32);
            }

            self.emit(VoteCast { voter: caller, vote: vote });
    }

        fn add_tokens_hashes(ref self: ContractState, tokens_hashes: Array<felt252>) {
            let caller: ContractAddress = get_caller_address();
            assert!(caller != self.admin_address.read(), "Only admin can add tokens hashes!");
            for token_hash in tokens_hashes {
                if (true){ // add preventing adding duplicated token hash
                    self.hashed_tokens.write(self.hashed_tokens_number.read(), token_hash);
                    self.hashed_tokens_number.write(self.hashed_tokens_number.read() + 1);
                }
            }
        }


        fn get_all_tokens_hashes(self: @ContractState) -> Array<felt252> {
            self._get_all_tokens_hashes()
    }

    }

    #[generate_trait]
    impl TokensImpl of TokensTrait {
    fn _get_all_tokens_hashes(self: @ContractState) -> Array<felt252> {
        let mut _hashed_tokens: Array<felt252> = ArrayTrait::new();
        let mut i = 0_u32;
        while i != self.hashed_tokens_number.read() {
            _hashed_tokens.append(self.hashed_tokens.read(i));
            i += 1;
        };
        _hashed_tokens
    }
    }
    

    #[generate_trait]
    impl AssertsImpl of AssertsTrait {
        fn _assert_user_not_voted(ref self: ContractState, address: ContractAddress) {
            let can_vote: bool = self.users_who_voted.read(address);
            assert!(!can_vote, "USER_ALREADY_VOTED");
        }

        fn _assert_token_hash_not_used(ref self: ContractState, token_hash: felt252) {
            let can_use: bool = self.used_tokens_hashes.read(token_hash);
            assert!(!can_use, "TOKEN_USED");
        }
    }

    #[generate_trait]
    impl VoteResultFunctionsImpl of VoteResultFunctionsTrait{
        fn _get_voting_result(self: @ContractState) -> (u32, u32) {
            let n_yes: u32 = self.yes_votes.read();
            let n_no: u32 = self.no_votes.read();
            
            (n_yes, n_no)
        }

        fn _get_voting_result_in_percentage(self: @ContractState) -> (u32, u32) {
            let n_yes: u32 = self.yes_votes.read();
            let n_no: u32 = self.no_votes.read();

            let total_votes: u32 = n_yes + n_no;

            if (total_votes == 0_u32) {
                return (0, 0);
            }
            let yes_percentage: u32 = (n_yes * 100_u32) / (total_votes);
            let no_percentage: u32 = (n_no * 100_u32) / (total_votes);

            (yes_percentage, no_percentage)
        }
    }
}