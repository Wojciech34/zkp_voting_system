from utils.config import (
    FACT_REGISTRY_SC_ADDRESS,
    PROOF_LAYOUT,
    STONE_VERSION,
    PROOF_COMMITMENT_HASH,
)


import subprocess as sp
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def verify_proof(
    fact_registry_address=FACT_REGISTRY_SC_ADDRESS,
    calldata_file=None,
    layout=PROOF_LAYOUT,
    hasher=PROOF_COMMITMENT_HASH["verifier"],
    stone_version=STONE_VERSION["verifier"],
    memory_verification="cairo1",
):

    cmd = [
        "../../verify-on-starknet.sh",
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
