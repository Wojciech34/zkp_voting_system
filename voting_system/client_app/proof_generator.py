"""
Generate ZK-STARK proof of given cairo program with input
"""

import os
import subprocess as sp
import logging

from utils.config import (
    PROOF_LAYOUT,
    PROOF_OF_WORK_BITS,
    STONE_VERSION,
    PROOF_COMMITMENT_HASH,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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
    output="serialized_proof.json",
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
