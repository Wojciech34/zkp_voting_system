from tests.example_voting_steps import admin_steps_setup, admin_steps_final
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def run_setup():
    sc_address = admin_steps_setup()
    return sc_address

def run_final(sc_address):
    admin_steps_final(sc_address)
