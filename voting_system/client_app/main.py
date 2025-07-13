# from ecdsa import SigningKey
#
# sk = SigningKey.generate()
# vk = sk.verifying_key
# signature = sk.sign(b"message")
# breakpoint()

from proof_generator import generate_stone_proof, serialize_proof
from proof_verify import verify_proof



#
# generate_stone_proof("program.cairo", program_input="[1 2]")

# generate_stone_proof("program.cairo",
#                      output="test_proof.json",
#                      program_input="[1]")

# serialize_proof("test_proof.json")

verify_proof(fact_registry_address="0x4ce7851f00b6c3289674841fd7a1b96b6fd41ed1edc248faccd672c26371b8c",
             calldata_file="serialized_proof_wrong.json",
             layout="recursive",
             hasher="keccak_160_lsb",
             stone_version="stone5",
             memory_verification="strict")