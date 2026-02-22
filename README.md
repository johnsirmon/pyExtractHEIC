# HEIC to PNG Converter

Extract HEIC photos from iCloud zip archives and convert them to PNG files.

## Quick Start

### Prerequisites

- Python 3.10+
- `pip`

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run (CLI)

```bash
python -m heic_converter \
  --zip-dir   ./zip     \
  --convert-dir ./convert
```

Place iCloud zip files (matching `*icloud*.zip`) in the `./zip` directory, then run the
command above.  Converted PNG files will appear in `./convert`.

Use `--help` for all options:

```bash
python -m heic_converter --help
```

### Run (legacy script)

```bash
python ConvertIphonePics.py
```

This expects `./zip`, `./extract`, and `./convert` directories relative to the script.

---

## How It Works

1. Each zip file matching `*icloud*.zip` in `--zip-dir` is opened.
2. Files inside the `iCloud Photos/` folder within the zip are extracted to a
   temporary directory.
3. Every `.heic` file is converted to `.png` and saved in `--convert-dir`.
4. The temporary extract directory is removed.

---

## Development

### Install dev dependencies

```bash
pip install -r requirements.txt
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

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs lint and tests on
every push and pull request.

---

## Project Structure

```
heic_converter/        # Main package
  __init__.py
  converter.py         # Core extraction & conversion logic
  cli.py               # argparse CLI entry point
tests/
  test_converter.py    # Unit tests for converter module
  test_cli.py          # Unit tests for CLI
ConvertIphonePics.py   # Legacy entry-point (calls heic_converter)
requirements.txt       # Runtime dependencies
pyproject.toml         # Build & tool configuration
.github/workflows/ci.yml
```

