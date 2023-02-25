
# setup to test
you will need to pip install the dependencies os, fnmatch, etc..
you will need to also copy a icloud zip file containing .HEIC files to the zip directory 
these are the files that will be extracted then converted to HEIC

# HEIC to PNG Converter

This code extracts HEIC files from a zip file, converts them to PNG, and deletes the extracted files.

## Directories

The following directories are set:

- Zip file directory: `zip`
- Extracted file directory: `extract`
- Converted file directory: `convert`

## Zip Files

The pattern for zip files is set as `*icloud*.zip`. The code loops through zip files, and if the zip file matches the pattern, it is opened. The code then loops through files in the zip file. If the file is not in the icloud photos folder, the icloud photos directory is removed from the file path. The file is then extracted to the extract directory.

## HEIC Files

The code loops through extracted files. If the file is a HEIC file, it is opened and converted to a PNG. The PNG is saved in the convert directory.

## Clean up

The extracted files are deleted, and the extract directory is deleted.
