import logging
import subprocess as sp
from config import (
    FACT_REGISTRY_SC_ADDRESS,
    PROOF_LAYOUT,
    STONE_VERSION,
    PROOF_COMMITMENT_HASH,
    PROOF_OF_WORK_BITS
)


def get_all_tokens_hashes(contract_address):
    cmd = [
        "sncast",
        "call",
        "--contract-address",
        contract_address,
        "--function",
        "get_all_tokens_hashes",
    ]

    try:
        logging.info("Getting all tokens hashes...")
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60)
        logging.info(res.decode())
        return res.decode()
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())
        raise e
    except Exception as e:
        logging.error(f"Unknown error occured: {e}")
        raise e


def vote(contract_address, token_hash, vote_):
    cmd = [
        "sncast",
        "invoke",
        "--contract-address",
        contract_address,
        "--function",
        "vote",
        "--arguments",
        f"{token_hash},{vote_}",
    ]

    try:
        logging.info("Submitting a vote...")
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60)
        logging.info(res.decode())
        return True
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())
        return False
    except Exception as e:
        logging.error(f"Unknown error occured: {e}")
        return False


def get_vote_status(contract_address):
    cmd = [
        "sncast",
        "call",
        "--contract-address",
        contract_address,
        "--function",
        "get_vote_status",
    ]

    try:
        logging.info("Getting vote status...")
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60)
        logging.info(res.decode())
        return res.decode()
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())
        raise e
    except Exception as e:
        logging.error(f"Unknown error occured: {e}")
        raise e


def generate_stone_proof(
    program_path,
    cairo_version="cairo1",
    program_input=None,
    layout=PROOF_LAYOUT,
    commitment_hash=PROOF_COMMITMENT_HASH["prover"],
    output="proof.json",
    proof_of_work_bits=PROOF_OF_WORK_BITS,
    stone_version=STONE_VERSION["prover"],
):

    cmd = [
        "stone-cli",
        "prove",
        "--cairo_program",
        program_path,
        "--cairo_version",
        cairo_version,
        "--layout",
        layout,
        "--commitment_hash",
        commitment_hash,
        "--output",
        output,
        "--proof_of_work_bits",
        str(proof_of_work_bits),
        "--stone_version",
        stone_version,
    ]
    if program_input:
        cmd += ["--program_input", program_input]

    logging.info("generating proof...")
    logging.info(" ".join(cmd))
    try:
        res = sp.check_output(cmd, stderr=sp.STDOUT)
        logging.info(res.decode())
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())


def serialize_proof(
    proof_path,
    network="starknet",
    serialization_type="monolith",
    output="serialized_proof2.json",
):

    cmd = [
        "stone-cli",
        "serialize-proof",
        "--proof",
        proof_path,
        "--network",
        network,
        "--serialization_type",
        serialization_type,
        "--output",
        output,
    ]

    logging.info("serializing proof...")
    _ = sp.check_output(cmd)
    logging.info(f"serialized proof: {proof_path}")


def verify_proof(
    fact_registry_address=FACT_REGISTRY_SC_ADDRESS,
    calldata_file=None,
    layout=PROOF_LAYOUT,
    hasher=PROOF_COMMITMENT_HASH["verifier"],
    stone_version=STONE_VERSION["verifier"],
    memory_verification="cairo1",
):

    cmd = [
        "./verify-on-starknet.sh",
        fact_registry_address,
        calldata_file,
        layout,
        hasher,
        stone_version,
        memory_verification,
    ]

    try:
        logging.info(f"Checking proof...\n{" ".join(cmd)}")
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60)
        logging.info(res.decode())
        return True
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())
        return False
    except Exception as e:
        logging.error(f"Unknown error occured: {e}")
        return False