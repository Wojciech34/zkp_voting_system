from utils.config import  FACT_REGISTRY_SC_ADDRESS


import subprocess as sp
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def verify_proof(fact_registry_address=FACT_REGISTRY_SC_ADDRESS,
                 calldata_file="serialized_proof.json",
                 layout="recursive",
                 hasher="keccak_160_lsb",
                 stone_version="stone5",
                 memory_verification="strict"):
    
    cmd = ["./verify-on-starknet.sh", fact_registry_address, calldata_file, layout, hasher, stone_version, memory_verification]
    
    try:
        logging.info("Checking proof...")
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60)
        logging.info(res.decode())
        return True
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())
        return False
    except Exception as e:
        logging.error(f"Unknown error occured: {e}")
        return False