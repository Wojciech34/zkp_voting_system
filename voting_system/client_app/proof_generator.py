"""
Generate ZK-STARK proof of given cairo program with input
"""
import subprocess as sp
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
# program_path = "program.cairo"




def generate_stone_proof(program_path,
                         cairo_version="cairo1",
                         program_input=None,
                         layout="starknet",
                         output="proof.json",
                         proof_of_work_bits="32",
                         stone_version="v6"
                         ):
    cmd = [
        "stone-cli", "prove", "--cairo_program", program_path, "--cairo_version",
        cairo_version, "--layout", layout, "--output", output, "--proof_of_work_bits",
        proof_of_work_bits, "--stone_version", stone_version
    ]
    if program_input:
        cmd += ["--program_input", program_input]

    logging.info("generating proof...")
    try:
        res = sp.check_output(cmd, stderr=sp.STDOUT)
        logging.info(res.decode())
    except sp.CalledProcessError as e:
        logging.error(e.output.decode())


def serialize_proof(proof_path,
                    network="starknet",
                    serialization_type="monolith",
                    output="serialized_proof.json",
                    ):

    cmd = [
        "stone-cli", "serialize-proof", "--proof", proof_path, "--network", network,
        "--serialization_type", serialization_type, "--output", output
    ]

    logging.info("serializing proof...")
    _ = sp.check_output(cmd)
    logging.info(f"serialized proof: {proof_path}")
