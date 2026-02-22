"""Tests for the heic_converter CLI."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

from PIL import Image

from heic_converter.cli import main


def _make_png_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (4, 4), color=(0, 128, 0)).save(buf, format="PNG")
    return buf.getvalue()


def _make_icloud_zip(path: Path, filenames: list[str]) -> Path:
    with zipfile.ZipFile(path, "w") as zf:
        for name in filenames:
            zf.writestr(f"iCloud Photos/{name}", _make_png_bytes())
    return path


class TestCLI:
    def test_returns_zero_on_success(self, tmp_path: Path) -> None:
        zip_dir = tmp_path / "zip"
        zip_dir.mkdir()
        _make_icloud_zip(zip_dir / "icloud_photos.zip", ["photo.HEIC"])

        rc = main([
            "--zip-dir", str(zip_dir),
            "--extract-dir", str(tmp_path / "extract"),
            "--convert-dir", str(tmp_path / "convert"),
        ])

        assert rc == 0
        assert (tmp_path / "convert" / "photo.png").exists()

    def test_returns_one_when_zip_dir_missing(self, tmp_path: Path) -> None:
        rc = main([
            "--zip-dir", str(tmp_path / "no_such_dir"),
            "--extract-dir", str(tmp_path / "extract"),
            "--convert-dir", str(tmp_path / "convert"),
        ])

        assert rc == 1
