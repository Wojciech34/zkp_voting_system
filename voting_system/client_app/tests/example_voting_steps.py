import time

from proof_generator import generate_stone_proof, serialize_proof
from proof_verify import verify_proof
from sc_interactions import (
    get_all_tokens_hashes,
    declare_sc,
    deploy_sc,
    add_tokens_hashes,
    vote,
    get_vote_status,
)


def admin_steps_setup():
    res = declare_sc()
    class_hash = [el.split(": ")[1] for el in res.split("\n") if "class_hash" in el][0]
    time.sleep(1)

    res = deploy_sc(class_hash)
    contract_address = [
        el.split(": ")[1] for el in res.split("\n") if "contract_address" in el
    ][0]
    time.sleep(1)

    add_tokens_hashes(
        contract_address,
        tokens_hashes=[
            "0x4759d339ba129b0922f008577d3029dcd00aa9da40fa8d2f748ddd36ed71261",
            "0x43efbb1923d35f4fff94f5a8236b811199b4d48eca1ffe7f0e6d4870733c5c0",
            "0x485446a579888a25821e2cc8cb935121b58cc5f258d4b80c194fdb7dd82800",
            "0x54b9cf9cb757b344313db9554533d5a74ef0283d359741f03fcddc29e3764b8",
        ],
    )
    return contract_address


def voter_steps_final(
    contract_address, vote_, token, token_hash, account_address, generate_proof=False
):
    all_tokens_hashes = get_all_tokens_hashes(contract_address)
    all_tokens_hashes = all_tokens_hashes.split("\n")[1].split(": ")[1]
    all_tokens_hashes = all_tokens_hashes[1:-1].split(", ")
    time.sleep(1)

    account_address_10 = int(account_address, 16)
    token_10 = int(token, 16)
    all_tokens_hashes_10 = [str(int(el, 16)) for el in all_tokens_hashes]

    # because generating proof takes much time, one may have already generated proofs for tests
    if generate_proof:
        # generate proof
        generate_stone_proof(
            "program.cairo",
            output="proof.json",
            program_input=f"[{account_address_10} {token_10} {" ".join(all_tokens_hashes_10)}]",
        )

        serialize_proof("proof.json")

    # verify proof and save it on integrity SC
    verify_proof(calldata_file="serialized_proof.json")
    time.sleep(1)

    vote(contract_address, token_hash, vote_)


def get_final_voting_result(contract_address):
    res = get_vote_status(contract_address)
    return res
