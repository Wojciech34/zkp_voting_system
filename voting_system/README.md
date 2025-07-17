# Starknet Development Notes

## Suggested Tools

- [asdf](https://asdf-vm.com/)
- [Scarb](https://docs.swmansion.com/scarb/) (can be installed via `asdf`)

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