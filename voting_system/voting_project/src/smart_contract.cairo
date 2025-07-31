// #[derive(Drop, Serde, Copy)]
// pub struct VoteTicket {
//     voter: ContractAddress,
//     ticket_number: u8,
// }

// use starknet::ContractAddress;


#[starknet::interface]
trait VoteTrait<T> {
    
    fn get_vote_status(self: @T) -> (u32, u32, u32, u32);

    // fn voter_can_vote(self: @T, user_address: ContractAddress) -> bool;

    // fn is_voter_registered(self: @T, address: ContractAddress) -> bool;

    fn vote(ref self: T, vote: u8);

    // fn send_ticket(ref self: T, user_address: ContractAddress) -> VoteTicket;

    fn add_allowed_voters_signatures(ref self: T, signatures: Array<felt252>);

    fn generate_token(ref self: T, signature: felt252);

    fn get_token(self: @T, signature: felt252) -> felt252;

    fn get_all_tokens_hashes(self: @T) -> Array<felt252>;

    fn remove_token(ref self: T, signature: felt252);

    fn set_voting_phase(ref self: T);

    // fn check_fact_hash(ref self: T, fact_hash: felt252, sec_bits: u32) -> bool;
    
}

#[starknet::contract]
mod Vote {
    // use starknet::storage::MutableVecTrait;
    //use super::VoteTrait;
use core::poseidon::PoseidonTrait;
    use core::hash::HashStateTrait;
    // use super::VoteTrait;
    use starknet::ContractAddress;
    use starknet::{get_caller_address, get_block_timestamp};
    use starknet::storage::{
        StoragePointerReadAccess, StoragePointerWriteAccess, StorageMapReadAccess,
        StorageMapWriteAccess, Map, Vec
    };
    use integrity::{Integrity, IntegrityWithConfig, calculate_fact_hash};
    // use super::VoteTicket;
    const YES: u8 = 1_u8;
    const NO: u8 = 0_u8;

    

    // use cartridge_vrf::IVrfProviderDispatcher;
    // use cartridge_vrf::IVrfProviderDispatcherTrait;
    // use cartridge_vrf::Source;

    #[storage]
    struct Storage {
        yes_votes: u32,
        no_votes: u32,
        vote_ticket_number: u32,
        // dict storing users who voted
        users_who_voted: Map::<ContractAddress, bool>,
        // registered_voter: Map<ContractAddress, bool>,
        allowed_signatures: Map<felt252, bool>,
        admin_address: ContractAddress,
        temp_proof: Vec<felt252>,

        hashed_tokens: Map::<u32, felt252>,
        hashed_tokens_number: u32,

        signature_to_token: Map::<felt252, felt252>,
        voting_phase_enabled: bool
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

        self.voting_phase_enabled.write(false);

        // self.allowed_signatures.write(10, true);
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    enum Event {
        VoteCast: VoteCast,
        UnauthorizedAttempt: UnauthorizedAttempt,
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

        // fn voter_can_vote(self: @ContractState, user_address: ContractAddress) -> bool {
        //     self.can_vote.read(user_address)
        // }

        // fn is_voter_registered(self: @ContractState, address:ContractAddress) -> bool {
        //     self.registered_voter.read(address)
        // }

        fn vote(ref self: ContractState, vote: u8) {
            assert!(self.voting_phase_enabled.read(), "Voting phase is not yet enabled and generating tokens is still possible");


            assert!(vote == NO || vote == YES, "Vote_0_OR_1");
            let caller: ContractAddress = get_caller_address();
            self._assert_user_not_voted(caller);
            let caller_felt252 : felt252 = caller.into();


            if false { // for debug purposes


            // verify that proof for caller address has been registered
            // required security bits
            let SECURITY_BITS = 70;
            // hash of a program, from which proof should be generated
            let program_hash = 0x59874649ccc5a0a15ee77538f1eb760acb88cab027a2d48f4246bf17b7b7694;
            // expected output of a program, which is [caller address, hashed_token1, hashed_token2 ... hashed_tokenN]
            let tokens_hashes = self._get_all_tokens_hashes();
            let mut output: Array<felt252> = ArrayTrait::new();
            
            output.append(caller_felt252);
            
            for token_hash in tokens_hashes {
                output.append(token_hash);
            }
            
            // with program hash and otput fact_hash can be calculated
            let fact_hash = calculate_fact_hash(program_hash, output.span());
            let integrity = Integrity::new();
            // check if fact_hash was registered
            let mut is_verified = false;
            if integrity.is_fact_hash_valid_with_security(fact_hash, SECURITY_BITS) {
                is_verified = true;
            }
            assert!(is_verified, "Account with this address did not register valid fact hash of possesing token");
            
            }

            self.users_who_voted.write(caller, true);
            if (vote == NO) {
                self.no_votes.write(self.no_votes.read() + 1_u32);
            }
            if (vote == YES) {
                self.yes_votes.write(self.yes_votes.read() + 1_u32);
            }

            self.emit(VoteCast { voter: caller, vote: vote });
        }

    //     fn send_ticket(ref self: ContractState, user_address: ContractAddress) -> VoteTicket {

    //     let vote_ticket = VoteTicket {voter: user_address, ticket_number: self.vote_ticket_number.read() };
    //     self.vote_ticket_number.write(self.vote_ticket_number.read() + 1_u8);
    //     vote_ticket

    // }
        fn add_allowed_voters_signatures(ref self: ContractState, signatures: Array<felt252>) {
            let caller: ContractAddress = get_caller_address();
            assert!(caller != self.admin_address.read(), "Only admin can add singatures!");
            for _signature in signatures {
                if (!self.allowed_signatures.read(_signature)){
                    self.allowed_signatures.write(_signature, true);
                }
                else {
                    println!("Signature {} is already added", _signature);
                }
            }
        }

        fn generate_token(ref self: ContractState, signature: felt252) {

            assert!(!self.voting_phase_enabled.read(), "Voting phase is enabled and generating tokens is no longer possible");
        
            assert!(self.allowed_signatures.read(signature), "You are not authorized to get a token!");

            // generate tokne basing on partially random assumptions

            let caller = get_caller_address();
            let timestamp = get_block_timestamp();

            let input1: felt252 = caller.into();
            let input2: felt252 = timestamp.into();

            let token = PoseidonTrait::new().update(input1).update(input2).finalize();
            self.signature_to_token.write(signature, token);

            let hashed_token = PoseidonTrait::new().update(token).finalize();
            self.hashed_tokens.write(self.hashed_tokens_number.read(), hashed_token);
            self.hashed_tokens_number.write(self.hashed_tokens_number.read() + 1_u32);
    }

        fn get_token(self: @ContractState, signature: felt252) -> felt252 {
            self.signature_to_token.read(signature)
    }

        fn get_all_tokens_hashes(self: @ContractState) -> Array<felt252> {
            self._get_all_tokens_hashes()
    }

        fn remove_token(ref self: ContractState, signature: felt252) {
            self.signature_to_token.write(signature, 0);
        }

        fn set_voting_phase(ref self: ContractState) {
            let caller: ContractAddress = get_caller_address();
            assert!(caller != self.admin_address.read(), "Only admin can set voting phase!");
            self.voting_phase_enabled.write(true);
        }


        // fn check_fact_hash(ref self: ContractState, fact_hash: felt252, sec_bits: u32) -> bool {
        //     let integrity = Integrity::new();
        //     let mut ret = true;
        //     if (!integrity.is_fact_hash_valid_with_security(fact_hash, sec_bits)){
        //         ret = false;
        //     }
        //     ret
        // }  
    }

    #[generate_trait]
    impl TokensImpl of TokensTrait {
    fn _get_all_tokens_hashes(self: @ContractState) -> Array<felt252> {
        let mut _hashed_tokens: Array<felt252> = ArrayTrait::new();
        let mut i = 0_u32;
        while i != self.hashed_tokens_number.read() {
            _hashed_tokens.append(self.hashed_tokens.read(i));
            i += 1;
        }
        _hashed_tokens
    }
    }
    

    #[generate_trait]
    impl AssertsImpl of AssertsTrait {
        fn _assert_user_not_voted(ref self: ContractState, address: ContractAddress) {
            let can_vote: bool = self.users_who_voted.read(address);
            assert!(!can_vote, "USER_ALREADY_VOTED");
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