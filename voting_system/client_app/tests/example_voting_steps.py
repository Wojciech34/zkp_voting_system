import time
import os

from proof_generator import generate_stone_proof, serialize_proof
from proof_verify import verify_proof
from sc_interactions import (get_token, generate_token, get_all_tokens_hashes, declare_sc,
                             deploy_sc, add_allowed_signatures, vote, get_vote_status, set_voting_phase)



def admin_steps_setup():
    res = declare_sc()
    class_hash = [el.split(": ")[1] for el in res.split("\n") if "class_hash" in el][0]
    time.sleep(1)

    res = deploy_sc(class_hash)
    contract_address = \
    [el.split(": ")[1] for el in res.split("\n") if "contract_address" in el][0]
    time.sleep(1)

    add_allowed_signatures(contract_address, allowed_signatures=["0x001", "0x002", "0x003", "0x004"])
    return contract_address


def admin_steps_final(contract_address):
    set_voting_phase(contract_address)


def voter_steps_setup(contract_address, signature):
    generate_token(contract_address, signature=signature)
    time.sleep(1)

    token = get_token(contract_address, signature=signature)
    token = token.split("\n")[1].split("[")[-1].split("]")[0]
    time.sleep(1)


def voter_steps_final(contract_address, vote_):
    all_tokens_hashes = get_all_tokens_hashes(contract_address)
    all_tokens_hashes = all_tokens_hashes.split("\n")[1].split(": ")[1]
    time.sleep(1)

    # generowanie dowodu
    # generate_stone_proof("program2.cairo",
    #                      output="test_proof2.json",
    #                      program_input="[123 2 12 123]")

    # serialize_proof("test_proof.json")

    # verify proof and save it on integrity SC
    # verify_proof(calldata_file="serialized_proof_correct.json")

    vote(contract_address, vote_)

def get_final_voting_result(contract_address):
    res = get_vote_status(contract_address)
    return res