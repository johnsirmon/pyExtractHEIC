"""Core logic for extracting HEIC files from iCloud zip archives and converting
them to PNG.
"""

from __future__ import annotations

import fnmatch
import logging
import shutil
import zipfile
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

logger = logging.getLogger(__name__)

_ICLOUD_FOLDER_PREFIX = "icloud photos/"
_ZIP_PATTERN = "*icloud*.zip"
_HEIC_PATTERN = "*.heic"


def extract_heic_from_zip(
    zip_path: Path,
    extract_dir: Path,
    *,
    icloud_prefix: str = _ICLOUD_FOLDER_PREFIX,
) -> list[Path]:
    """Extract HEIC files from a single zip archive into *extract_dir*.

    Files inside the zip that live under *icloud_prefix* are flattened into
    *extract_dir* (the prefix is stripped).

    Returns a list of extracted file paths.
    """
    extracted: list[Path] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            if fnmatch.fnmatch(info.filename.lower(), f"{icloud_prefix}*"):
                info.filename = Path(info.filename).name
                if not info.filename:
                    continue
                dest = Path(zf.extract(info, extract_dir))
                extracted.append(dest)
                logger.debug("Extracted %s", dest)
    logger.info("Extracted %d file(s) from %s", len(extracted), zip_path.name)
    return extracted


def convert_heic_to_png(heic_path: Path, output_dir: Path) -> Path:
    """Convert a single HEIC file to PNG and save it in *output_dir*.

    Returns the path of the written PNG file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / (heic_path.stem + ".png")
    with Image.open(heic_path) as img:
        img.save(png_path, format="PNG")
    logger.info("Converted %s → %s", heic_path.name, png_path.name)
    return png_path


def convert_directory(
    extract_dir: Path,
    convert_dir: Path,
) -> list[Path]:
    """Convert all HEIC files in *extract_dir* to PNG files in *convert_dir*.

    Returns a list of created PNG paths.
    """
    converted: list[Path] = []
    for path in extract_dir.iterdir():
        if fnmatch.fnmatch(path.name.lower(), _HEIC_PATTERN):
            png = convert_heic_to_png(path, convert_dir)
            converted.append(png)
    return converted


def process_zip_dir(
    zip_dir: Path,
    extract_dir: Path,
    convert_dir: Path,
    *,
    zip_pattern: str = _ZIP_PATTERN,
) -> tuple[list[Path], list[Path]]:
    """Process all matching zip files in *zip_dir*.

    1. Extract HEIC files from each zip to *extract_dir*.
    2. Convert every HEIC in *extract_dir* to PNG in *convert_dir*.
    3. Remove *extract_dir* and its contents.

    Returns ``(extracted_files, converted_files)``.
    """
    if not zip_dir.is_dir():
        raise FileNotFoundError(f"Zip directory not found: {zip_dir}")

    extract_dir.mkdir(parents=True, exist_ok=True)
    convert_dir.mkdir(parents=True, exist_ok=True)

    all_extracted: list[Path] = []
    for zip_file in zip_dir.iterdir():
        if fnmatch.fnmatch(zip_file.name.lower(), zip_pattern.lower()):
            extracted = extract_heic_from_zip(zip_file, extract_dir)
            all_extracted.extend(extracted)

    converted = convert_directory(extract_dir, convert_dir)

    shutil.rmtree(extract_dir)
    logger.info("Removed temporary extract directory: %s", extract_dir)

    return all_extracted, converted
