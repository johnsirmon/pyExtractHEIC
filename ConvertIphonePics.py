# This code extracts HEIC files from a zip file, converts them to PNG, and deletes the extracted files.
# The zip file directory is set as zip_dir_path. The extracted file directory is set as extract_dir_path. The converted file directory is set as convert_dir_path.
# A pattern is set for zip files. The pattern is zip_pattern.
# The loop loops through zip files. If the zip file matches the pattern, the zip file is opened. The loop then loops through files in the zip file. If the file is not in the icloud photos folder, the icloud photos directory is removed from the file path. The file is then extracted to the extract directory.
# The loop loops through extracted files. If the file is a HEIC file, the file is opened. The file is then converted to a PNG and saved in the convert directory.
# The extracted files are deleted.
# The extract directory is deleted.

import os
import zipfile
import fnmatch
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF opener with Pillow
register_heif_opener()

# Set paths for zip file directory, extracted file directory, and converted file directory
zip_dir_path = r"\zip"
zip_dir_path = zip_dir_path.replace("\\", "/")

extract_dir_path = r"\extract"
extract_dir_path = extract_dir_path.replace("\\", "/")

convert_dir_path = r"\convert"
convert_dir_path = convert_dir_path.replace("\\", "/")

# Set pattern for zip files
zip_pattern = "*icloud*.zip"

# Loop through zip files
for filename in os.listdir(zip_dir_path):
    # If zip file matches pattern
    if fnmatch.fnmatch(filename, zip_pattern):
        # Open zip file
        with zipfile.ZipFile(os.path.join(zip_dir_path, filename), 'r') as zip_ref:
            # Loop through files in zip file
            for zip_info in zip_ref.infolist():
                # If file is not in icloud photos folder
                if not fnmatch.fnmatch(zip_info.filename, "icloud photos/*"):
                    # Remove icloud photos directory from file path
                    zip_info.filename = os.path.basename(zip_info.filename)
                    # Extract file
                    zip_ref.extract(zip_info, extract_dir_path)
        print(f"Extracted {filename} to {extract_dir_path} ")

# Loop through extracted files
for filename in os.listdir(extract_dir_path):
    # If file is a HEIC file
    if fnmatch.fnmatch(filename, "*.heic"):
        # Open file
        with open(os.path.join(extract_dir_path, filename), "rb") as f:
            # Convert file to PNG
            im = Image.open(f)
            im.save(os.path.join(convert_dir_path, os.path.splitext(filename)[0] + ".png"), format="PNG")
        print(f"Converted {filename} to PNG")

# Delete extracted files
os.rmdir(extract_dir_path)
print("Deleted extract directory")
