from tests.example_voting_steps import admin_steps_setup
import os


def run_setup():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(SCRIPT_DIR)

    sc_address = admin_steps_setup()
    return sc_address
