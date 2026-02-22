"""Command-line interface for heic_converter."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .converter import process_zip_dir


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="heic-converter",
        description="Extract HEIC files from iCloud zip archives and convert to PNG.",
    )
    parser.add_argument(
        "--zip-dir",
        type=Path,
        default=Path("zip"),
        help="Directory containing iCloud zip files (default: ./zip)",
    )
    parser.add_argument(
        "--extract-dir",
        type=Path,
        default=Path("extract"),
        help="Temporary directory for extracted files (default: ./extract)",
    )
    parser.add_argument(
        "--convert-dir",
        type=Path,
        default=Path("convert"),
        help="Output directory for converted PNG files (default: ./convert)",
    )
    parser.add_argument(
        "--zip-pattern",
        default="*icloud*.zip",
        help='Glob pattern for zip files (default: "*icloud*.zip")',
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (DEBUG) logging",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    try:
        extracted, converted = process_zip_dir(
            args.zip_dir,
            args.extract_dir,
            args.convert_dir,
            zip_pattern=args.zip_pattern,
        )
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Extracted {len(extracted)} file(s), converted {len(converted)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
