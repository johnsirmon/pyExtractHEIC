# pyExtractHEIC — HEIC to PNG Converter

![CI](https://github.com/johnsirmon/pyExtractHEIC/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Extract HEIC photos from iCloud zip archives and convert them to PNG files with a single command.

---

## Background

**HEIC** (High Efficiency Image Container) is the default photo format on iPhones running iOS 11 and later. While it offers better compression than JPEG, it is not universally supported — many apps, websites, and older tools expect JPEG or PNG.

When you export photos from **iCloud.com**, Apple packages them as one or more zip archives with names like `iCloud Photos - Part 1.zip`. Inside each zip, your photos are stored under an `iCloud Photos/` folder as `.heic` files.

**pyExtractHEIC** automates the tedious manual workflow of:
1. Unzipping each archive
2. Finding all `.heic` files
3. Converting them to widely-compatible `.png` files

---

## Quick Start

### Prerequisites

- Python 3.10 or later
- `pip`

### Install dependencies

```bash
pip install -r requirements.txt
```

### Export your photos from iCloud

1. Go to [icloud.com](https://www.icloud.com) → **Photos**
2. Select the photos you want, then click the download button
3. iCloud will prepare one or more zip files named like `iCloud Photos - Part 1.zip`
4. Save those zip files into a local folder (e.g. `./zip`)

### Run (CLI)

```bash
python -m heic_converter \
  --zip-dir   ./zip     \
  --convert-dir ./convert
```

Converted `.png` files will appear in `./convert`.  Use `--help` to see all options:

```bash
python -m heic_converter --help
```

### Run (installed console script)

If you install the package (`pip install -e .`), a `heic-converter` command becomes available:

```bash
heic-converter --zip-dir ./zip --convert-dir ./convert
```

### Run (legacy script)

```bash
python ConvertIphonePics.py
```

This expects `./zip`, `./extract`, and `./convert` directories next to the script.  It is kept for backward compatibility; prefer the CLI above for new use.

---

## How It Works

1. Every file in `--zip-dir` whose name matches the glob `*icloud*.zip` is opened.
2. Entries stored under the `iCloud Photos/` folder inside the zip are extracted to a
   temporary directory (`--extract-dir`, deleted automatically when done).
3. Every `.heic` file in the temporary directory is converted to `.png` and saved in
   `--convert-dir`.
4. The temporary extract directory is removed.

---

## CLI Reference

| Flag | Default | Description |
|---|---|---|
| `--zip-dir PATH` | `./zip` | Folder containing the iCloud zip archives |
| `--extract-dir PATH` | `./extract` | Temporary folder for extraction (deleted after conversion) |
| `--convert-dir PATH` | `./convert` | Output folder for converted PNG files |
| `--zip-pattern GLOB` | `*icloud*.zip` | Glob pattern used to select zip files |
| `-v` / `--verbose` | off | Enable DEBUG-level logging |

---

## Development

### Install dev dependencies

```bash
pip install -e .
pip install pytest ruff
```

### Lint

```bash
ruff check heic_converter/ tests/
```

### Test

```bash
pytest
```

### CI

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs lint and tests on every push and pull request.

---

## Project Structure

```
heic_converter/        # Main package
  __init__.py
  __main__.py          # Enables `python -m heic_converter`
  converter.py         # Core extraction & conversion logic
  cli.py               # argparse CLI entry point
tests/
  test_converter.py    # Unit tests for converter module
  test_cli.py          # Unit tests for CLI
ConvertIphonePics.py   # Legacy entry-point (delegates to heic_converter)
requirements.txt       # Runtime dependencies (Pillow, pillow-heif)
pyproject.toml         # Build & tool configuration
.github/workflows/ci.yml
```

---

## Opportunities to Improve

The following enhancements are not yet implemented but would make the tool more useful:

| Area | Idea |
|---|---|
| **Output formats** | Add a `--format` flag to support JPEG output in addition to PNG |
| **Parallel conversion** | Use `concurrent.futures.ThreadPoolExecutor` to convert multiple files at once — helpful for large photo libraries |
| **Resilient error handling** | Wrap per-file conversion in a `try/except` so one corrupt file does not abort the entire batch; log warnings instead |
| **Progress bar** | Add a `tqdm` progress bar for large batches to give visual feedback |
| **Preserve metadata** | Copy EXIF metadata (date taken, GPS, camera model) from the source HEIC to the output PNG using `piexif` |
| **Duplicate detection** | Skip conversion if a PNG with the same stem already exists in the output directory, avoiding redundant work on re-runs |
| **Configurable zip folder** | Expose `--icloud-prefix` as a CLI flag so users can handle zips with a different internal folder structure |
| **Dry-run mode** | Add a `--dry-run` flag to list what would be converted without writing any files |
| **JPEG input** | Extend the tool to also convert any `.jpg`/`.jpeg` files found in the archive for a one-stop photo normalisation workflow |

