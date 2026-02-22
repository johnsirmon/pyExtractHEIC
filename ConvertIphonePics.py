# This code extracts HEIC files from a zip file, converts them to PNG, and deletes the extracted files.
# The zip file directory is set as zip_dir_path. The extracted file directory is set as extract_dir_path. The converted file directory is set as convert_dir_path.
# A pattern is set for zip files. The pattern is zip_pattern.
# The loop loops through zip files. If the zip file matches the pattern, the zip file is opened. The loop then loops through files in the zip file. If the file is in the icloud photos folder, the icloud photos directory is removed from the file path. The file is then extracted to the extract directory.
# The loop loops through extracted files. If the file is a HEIC file, the file is opened. The file is then converted to a PNG and saved in the convert directory.
# The extracted files are deleted.
# The extract directory is deleted.

import os
import shutil
import zipfile
import fnmatch
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF opener with Pillow
register_heif_opener()

# Set paths for zip file directory, extracted file directory, and converted file directory
# Paths are relative to the script's directory
script_dir = Path(__file__).parent
zip_dir_path = script_dir / "zip"
extract_dir_path = script_dir / "extract"
convert_dir_path = script_dir / "convert"

# Create output directories if they don't exist
extract_dir_path.mkdir(parents=True, exist_ok=True)
convert_dir_path.mkdir(parents=True, exist_ok=True)

# Set pattern for zip files (matched case-insensitively)
zip_pattern = "*icloud*.zip"

# Loop through zip files
for filename in os.listdir(zip_dir_path):
    # If zip file matches pattern (case-insensitive)
    if fnmatch.fnmatch(filename.lower(), zip_pattern.lower()):
        # Open zip file
        with zipfile.ZipFile(zip_dir_path / filename, 'r') as zip_ref:
            # Loop through files in zip file
            for zip_info in zip_ref.infolist():
                # If file is in icloud photos folder
                if fnmatch.fnmatch(zip_info.filename.lower(), "icloud photos/*"):
                    # Remove icloud photos directory from file path
                    zip_info.filename = os.path.basename(zip_info.filename)
                    # Extract file
                    zip_ref.extract(zip_info, extract_dir_path)
        print(f"Extracted {filename} to {extract_dir_path}")

# Loop through extracted files
for filename in os.listdir(extract_dir_path):
    # If file is a HEIC file (case-insensitive match)
    if fnmatch.fnmatch(filename.lower(), "*.heic"):
        # Open file and convert to PNG
        with Image.open(extract_dir_path / filename) as im:
            png_filename = Path(filename).stem + ".png"
            im.save(convert_dir_path / png_filename, format="PNG")
        print(f"Converted {filename} to PNG")

# Delete extract directory and all its contents
shutil.rmtree(extract_dir_path)
print("Deleted extract directory")