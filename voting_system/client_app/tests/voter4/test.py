from tests.example_voting_steps import voter_steps_final
import os


def run_final(contract_address, token, token_hash, account_address):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(SCRIPT_DIR)

    voter_steps_final(contract_address, "1", token, token_hash, account_address)
