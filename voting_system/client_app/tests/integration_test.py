import time
import os

from proof_generator import generate_stone_proof, serialize_proof
from proof_verify import verify_proof
from sc_interactions import (get_token, generate_token, get_all_tokens_hashes, declare_sc,
                             deploy_sc, add_allowed_signatures, vote, get_vote_status, set_voting_phase)

# before executing test ensure katana is started

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

res = declare_sc()
class_hash = [el.split(": ")[1] for el in res.split("\n") if "class_hash" in el][0]
time.sleep(1)

res = deploy_sc(class_hash)
contract_address = [el.split(": ")[1] for el in res.split("\n") if "contract_address" in el][0]
time.sleep(1)

add_allowed_signatures(contract_address, allowed_signatures=["0x123", "0x123456"])
time.sleep(1)

generate_token(contract_address, signature="0x123")
time.sleep(1)

token = get_token(contract_address, signature="0x123")
token = token.split("\n")[1].split("[")[-1].split("]")[0]
time.sleep(1)

all_tokens_hashes = get_all_tokens_hashes(contract_address)
all_tokens_hashes = all_tokens_hashes.split("\n")[1].split(": ")[1]
time.sleep(1)

set_voting_phase(contract_address)
time.sleep(1)

# breakpoint()

# private i public input, czy da sie to robic w stone-cli jak przekazywac argumenty
# generowanie dowodu
# generate_stone_proof("program2.cairo",
#                      output="test_proof2.json",
#                      program_input="[123 2 12 123]")

# serialize_proof("test_proof.json")

# verify proof and save it on integrity SC
# verify_proof(calldata_file="serialized_proof_correct.json")

vote(contract_address,"0")
time.sleep(1)
res = get_vote_status(contract_address)
print(res)