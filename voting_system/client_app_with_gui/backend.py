from utils import get_all_tokens_hashes, generate_stone_proof, serialize_proof, verify_proof, vote, get_vote_status
import time


def submit_vote(token, token_hash, vote_, contract_address, account_address):

    all_tokens_hashes = get_all_tokens_hashes(contract_address)
    all_tokens_hashes = all_tokens_hashes.split("\n")[1].split(": ")[1]
    all_tokens_hashes = all_tokens_hashes[1:-1].split(", ")
    time.sleep(1)

    account_address_10 = int(account_address, 16)
    token_10 = int(token, 16)
    all_tokens_hashes_10 = [str(int(el, 16)) for el in all_tokens_hashes]

    # because generating proof takes much time, one may have already generated proof
    if True:
        # generate proof
        generate_stone_proof(
            "program.cairo",
            output="proof.json",
            program_input=f"[{account_address_10} {token_10} {" ".join(all_tokens_hashes_10)}]",
        )
        # serialize proof
        serialize_proof("proof.json")

    # verify proof and save it on integrity SC
    verify_proof(calldata_file="serialized_proof.json")
    time.sleep(1)

    vote(contract_address, token_hash, vote_)


def get_vote_status_(contract_address):
    res = get_vote_status(contract_address)
    print(res)
    res = res.split(": ")[-1]
    res = res.replace("[", "").replace("]", "")
    print(res)
    res = [int(el, 16) for el in res.split(",")]
    return f"Liczba głosów 1 / Liczba głosów 0 / Procent głosów 1 / Procent głosów 0\n{res}"


