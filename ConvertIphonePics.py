"""Backward-compatible entry point.

This script is retained for users who ran it directly before the refactor.
All logic now lives in the ``heic_converter`` package.  Run it as:

    python ConvertIphonePics.py

Or use the new CLI for more options:

    python -m heic_converter --help
"""

import logging
import sys
from pathlib import Path

from heic_converter.converter import process_zip_dir

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

script_dir = Path(__file__).parent
extracted, converted = process_zip_dir(
    script_dir / "zip",
    script_dir / "extract",
    script_dir / "convert",
)
print(f"Extracted {len(extracted)} file(s), converted {len(converted)} file(s).")
sys.exit(0)