from tests.example_voting_steps import voter_steps_setup, voter_steps_final
import os


def run_setup(contract_address):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(SCRIPT_DIR)

    voter_steps_setup(contract_address, "0x002")


def run_final(contract_address):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(SCRIPT_DIR)

    voter_steps_final(contract_address, "0")