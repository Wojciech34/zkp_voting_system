FACT_REGISTRY_SC_ADDRESS = (
    "0x4ce7851f00b6c3289674841fd7a1b96b6fd41ed1edc248faccd672c26371b8c"
)

# Proof params
PROOF_LAYOUT = "starknet"
PROOF_OF_WORK_BITS = 32
STONE_VERSION = {
    "prover": "v6",
    "verifier": "stone6",
}
# The same hash but under different names
PROOF_COMMITMENT_HASH = {
    "prover": "keccak256-masked160-lsb",
    "verifier": "keccak_160_lsb",
}
