Suggested Tools
 asdf
 scarb (can install via asdf)

 Stakrnet RPC Provider https://blastapi.io/
 Starknet Sequencer https://dojoengine.org/toolchain/katana

Stark local blockchain network
katana --dev --fork.provider https://starknet-sepolia.blastapi.io/API-KEY/rpc/v0_8 --explorer
note: with compability issues check required starknet rpc version, suggested one is 0.8

To compile smart contract classes in voting_project directory run
scarb build

note when facing issues with cairo extension for vs code, ensure that path to language server is set correctly 
(for  example ~/.asdf/installs/scarb/2.11.4/bin/scarb-cairo-language-server)


To declare contract use
sncast declare --contract-name Vote
Note: contract-name is mod name, the one with #[starknet::contract] header
Then deploy smart contrakt
sncast deploy --class-hash <class_hash>


To interact with smart contract
not modfifying contract state
sncast call --contract-address <contract_address> --function <function_name> --arguments <arguments>
modifying contract state
sncast invoke 