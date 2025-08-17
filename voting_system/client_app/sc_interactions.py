import subprocess as sp
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

SC_REPO_PATH = (
    "/home/wojtek/cairo_projects/tech-zkpdual-cr/voting_system/voting_project"
)


def add_tokens_hashes(contract_address, tokens_hashes):
    arguments = ["array![" + ", ".join(tokens_hashes) + "]"]
    cmd = [
        "sncast",
        "invoke",
        "--contract-address",
        contract_address,
        "--function",
        "add_tokens_hashes",
        "--arguments",
        *arguments,
    ]

    try:
        logging.info("As an admin adding allowed token hashes...")
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60)
        logging.info(res.decode())
        return True
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())
        raise e
    except Exception as e:
        logging.error(f"Unknown error occured: {e}")
        raise e


def generate_token(contract_address, signature):
    cmd = [
        "sncast",
        "invoke",
        "--contract-address",
        contract_address,
        "--function",
        "generate_token",
        "--arguments",
        signature,
    ]

    try:
        logging.info("Generating token...")
        # breakpoint()
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60)
        logging.info(res.decode())
        return True
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())
        raise e
    except Exception as e:
        logging.error(f"Unknown error occured: {e}")
        raise e


def get_token(contract_address, signature):
    cmd = [
        "sncast",
        "call",
        "--contract-address",
        contract_address,
        "--function",
        "get_token",
        "--arguments",
        signature,
    ]

    try:
        logging.info("Getting token...")
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60)
        logging.info(res.decode())
        return res.decode()
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())
        raise e
    except Exception as e:
        logging.error(f"Unknown error occured: {e}")
        raise e


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


def set_voting_phase(contract_address):
    cmd = [
        "sncast",
        "invoke",
        "--contract-address",
        contract_address,
        "--function",
        "set_voting_phase",
    ]

    try:
        logging.info("Setting voting phase...")
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60)
        logging.info(res.decode())
        return True
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


def declare_sc():
    cmd = ["sncast", "declare", "--contract-name", "Vote"]

    try:
        logging.info("Declaring smart contract...")
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60, cwd=SC_REPO_PATH)
        logging.info(res.decode())
        return res.decode()
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())
        raise e
    except Exception as e:
        logging.error(f"Unknown error occured: {e}")
        raise e


def deploy_sc(class_hash):
    cmd = ["sncast", "deploy", "--class-hash", class_hash]

    try:
        logging.info("Deploying smart contract...")
        res = sp.check_output(cmd, stderr=sp.STDOUT, timeout=60, cwd=SC_REPO_PATH)
        logging.info(res.decode())
        return res.decode()
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())
        raise e
    except Exception as e:
        logging.error(f"Unknown error occured: {e}")
        raise e
