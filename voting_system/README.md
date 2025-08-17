# Starknet Development Notes

## Suggested Tools

- [asdf](https://asdf-vm.com/)
- [Scarb](https://docs.swmansion.com/scarb/) (can be installed via `asdf`)
```bash
asdf plugin add scarb
asdf install scarb 2.11.4
asdf set -u scarb 2.11.4
```
- [Sncast](https://foundry-rs.github.io/starknet-foundry)
```bash
asdf plugin add starknet-foundry
asdf install starknet-foundry 0.42.0
asdf set -u starknet-foundry 0.42.0
```

## Starknet RPC Provider

- [BlastAPI](https://blastapi.io/)

## Blockchain sequencer
- [Katana (Dojo)](https://dojoengine.org/toolchain/katana)

## Running a Local Starknet Blockchain Network

```bash
katana --dev --fork.provider https://starknet-sepolia.blastapi.io/API-KEY/rpc/v0_8 --explorer
```

**Note:**  
Check for compatibility issues with your Starknet RPC version. The suggested version is `v0.8`.

## Compiling Smart Contracts

To compile smart contract classes in the `voting_project` directory:

```bash
scarb build
```

**VS Code Tip:**  
If you face issues with the Cairo extension in VS Code, ensure the language server path is set correctly.  
Example path:

```bash
~/.asdf/installs/scarb/2.11.4/bin/scarb-cairo-language-server
```

## Declaring and Deploying Contracts

> **Note:** run following commands in voting_project directory.

### Declare Contract

```bash
sncast declare --contract-name Vote
```

> **Note:** `contract-name` refers to the module name marked with `#[starknet::contract]`.

### Deploy Contract

```bash
sncast deploy --class-hash <class_hash>
```

## Interacting with Smart Contracts

### Read-Only (No State Modification)

```bash
sncast call --contract-address <contract_address> --function <function_name> --arguments <arguments>
```

### State-Changing (Modifies Contract State)

```bash
sncast invoke --contract-address <contract_address> --function <function_name> --arguments <arguments>
```
## Adding accounts
```bash
sncast account create --name <account_name>
```
**Notes:**
- That command will create accounts folder if not created previously in path (~/.starknet_accounts/starknet_open_zeppelin_accounts.json).
- Easy way to use such account is to copy private and public key and account address from some predeployed account.
- After creating account you probably want to change the "account" variable in the file `voting_system/voting_project/snfoundry.toml`.

## Running Tests
To run test in client_app directory run

```bash
PYTHONPATH=. python3 tests/example_voting_test.py
```
or
```bash
PYTHONPATH=. python3 tests/integration_test.py
```
**Notes:**
- You shall change the variable `STONE_CLI_PATH` from file `voting_system/client_app/proof_generator.py` to your own path.
- You shall change the variable `SC_REPO_PATH` from file `voting_system/client_app/sc_interactions.py` to your own path.
