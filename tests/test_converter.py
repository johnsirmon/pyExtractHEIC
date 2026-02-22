"""Tests for heic_converter."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pytest
from PIL import Image

from heic_converter.converter import (
    convert_directory,
    convert_heic_to_png,
    extract_heic_from_zip,
    process_zip_dir,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_png_bytes(size: tuple[int, int] = (4, 4)) -> bytes:
    """Return bytes of a tiny valid PNG image (used as a stand-in for HEIC)."""
    buf = io.BytesIO()
    Image.new("RGB", size, color=(255, 0, 0)).save(buf, format="PNG")
    return buf.getvalue()


def _make_zip(path: Path, members: dict[str, bytes]) -> Path:
    """Create a zip at *path* containing the given filename→bytes mapping."""
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    return path


# ---------------------------------------------------------------------------
# extract_heic_from_zip
# ---------------------------------------------------------------------------

class TestExtractHeicFromZip:
    def test_extracts_files_inside_icloud_folder(self, tmp_path: Path) -> None:
        zip_path = _make_zip(
            tmp_path / "photos.zip",
            {
                "iCloud Photos/IMG_001.HEIC": b"fake heic data",
                "iCloud Photos/IMG_002.HEIC": b"fake heic data 2",
                "iCloud Photos/":  b"",  # directory entry – should be skipped
            },
        )
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()

        extracted = extract_heic_from_zip(zip_path, extract_dir)

        names = {p.name for p in extracted}
        assert "IMG_001.HEIC" in names
        assert "IMG_002.HEIC" in names

    def test_ignores_files_outside_icloud_folder(self, tmp_path: Path) -> None:
        zip_path = _make_zip(
            tmp_path / "photos.zip",
            {
                "iCloud Photos/IMG_001.HEIC": b"heic",
                "README.txt": b"readme",
                "metadata/info.json": b"{}",
            },
        )
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()

        extracted = extract_heic_from_zip(zip_path, extract_dir)

        names = {p.name for p in extracted}
        assert "IMG_001.HEIC" in names
        assert "README.txt" not in names
        assert "info.json" not in names

    def test_case_insensitive_folder_match(self, tmp_path: Path) -> None:
        """Prefix matching should be case-insensitive."""
        zip_path = _make_zip(
            tmp_path / "photos.zip",
            {"ICLOUD PHOTOS/IMG_001.HEIC": b"heic"},
        )
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()

        extracted = extract_heic_from_zip(zip_path, extract_dir)

        assert len(extracted) == 1
        assert extracted[0].name == "IMG_001.HEIC"

    def test_empty_zip_returns_empty_list(self, tmp_path: Path) -> None:
        zip_path = _make_zip(tmp_path / "empty.zip", {})
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()

        extracted = extract_heic_from_zip(zip_path, extract_dir)

        assert extracted == []


# ---------------------------------------------------------------------------
# convert_heic_to_png
# ---------------------------------------------------------------------------

class TestConvertHeicToPng:
    def test_converts_png_source_to_png(self, tmp_path: Path) -> None:
        """Use a PNG as a stand-in (Pillow can open it); output must be PNG."""
        src = tmp_path / "photo.heic"
        src.write_bytes(_make_png_bytes())
        out_dir = tmp_path / "out"

        result = convert_heic_to_png(src, out_dir)

        assert result.exists()
        assert result.suffix.lower() == ".png"
        assert result.stem == "photo"
        with Image.open(result) as img:
            assert img.format == "PNG"

    def test_creates_output_dir_if_missing(self, tmp_path: Path) -> None:
        src = tmp_path / "photo.heic"
        src.write_bytes(_make_png_bytes())
        out_dir = tmp_path / "does" / "not" / "exist"

        result = convert_heic_to_png(src, out_dir)

        assert result.exists()


# ---------------------------------------------------------------------------
# convert_directory
# ---------------------------------------------------------------------------

class TestConvertDirectory:
    def test_converts_all_heic_files(self, tmp_path: Path) -> None:
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()
        convert_dir = tmp_path / "convert"

        (extract_dir / "IMG_001.HEIC").write_bytes(_make_png_bytes())
        (extract_dir / "IMG_002.heic").write_bytes(_make_png_bytes())
        (extract_dir / "notes.txt").write_text("ignored")

        converted = convert_directory(extract_dir, convert_dir)

        assert len(converted) == 2
        stems = {p.stem for p in converted}
        assert "IMG_001" in stems
        assert "IMG_002" in stems

    def test_skips_non_heic_files(self, tmp_path: Path) -> None:
        extract_dir = tmp_path / "extract"
        extract_dir.mkdir()
        convert_dir = tmp_path / "convert"

        (extract_dir / "photo.jpg").write_bytes(_make_png_bytes())

        converted = convert_directory(extract_dir, convert_dir)

        assert converted == []


# ---------------------------------------------------------------------------
# process_zip_dir
# ---------------------------------------------------------------------------

class TestProcessZipDir:
    def _make_icloud_zip(self, path: Path, filenames: list[str]) -> Path:
        members = {f"iCloud Photos/{n}": _make_png_bytes() for n in filenames}
        return _make_zip(path, members)

    def test_end_to_end(self, tmp_path: Path) -> None:
        zip_dir = tmp_path / "zip"
        zip_dir.mkdir()
        self._make_icloud_zip(zip_dir / "icloud_photos.zip", ["A.HEIC", "B.HEIC"])

        extract_dir = tmp_path / "extract"
        convert_dir = tmp_path / "convert"

        extracted, converted = process_zip_dir(zip_dir, extract_dir, convert_dir)

        assert len(extracted) == 2
        assert len(converted) == 2
        # Extract dir is cleaned up
        assert not extract_dir.exists()

    def test_raises_if_zip_dir_missing(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            process_zip_dir(
                tmp_path / "nonexistent",
                tmp_path / "extract",
                tmp_path / "convert",
            )

    def test_no_matching_zips_returns_empty(self, tmp_path: Path) -> None:
        zip_dir = tmp_path / "zip"
        zip_dir.mkdir()
        (zip_dir / "unrelated.zip").write_bytes(b"")

        extract_dir = tmp_path / "extract"
        convert_dir = tmp_path / "convert"

        extracted, converted = process_zip_dir(zip_dir, extract_dir, convert_dir)

        assert extracted == []
        assert converted == []
