import os
from pathlib import Path
from butler import tidy

def test_organize_directory_moves_files(tmp_path):
    """
    Test that files are correctly moved into subfolders based on extension.
    'tmp_path' is a built-in pytest fixture that creates a temporary directory.
    """
    # 1. SETUP: Create a fake environment
    # Create a messy file structure in the temp folder
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "document.pdf").touch()
    (tmp_path / "song.mp3").touch() # We don't have a folder for this in our map yet!

    # 2. ACTION: Run our code against the temp folder
    # We pass the string version of the path, just like the CLI does
    tidy.organize_directory(str(tmp_path))

    # 3. ASSERTION: Check if the Butler did his job

    # Check if 'Images' folder exists and contains the jpg
    assert (tmp_path / "Images").exists()
    assert (tmp_path / "Images" / "photo.jpg").exists()

    # Check if 'Documents' folder exists and contains the pdf
    assert (tmp_path / "Documents").exists()
    assert (tmp_path / "Documents" / "document.pdf").exists()

    # Check that the original files are gone from the root
    assert not (tmp_path / "photo.jpg").exists()
    assert not (tmp_path / "document.pdf").exists()

def test_unknown_extension_goes_to_misc(tmp_path):
    """
    Test that extensions we didn't define go to 'Misc'.
    """
    (tmp_path / "random.data").touch()

    tidy.organize_directory(str(tmp_path))

    assert (tmp_path / "Misc").exists()
    assert (tmp_path / "Misc" / "random.data").exists()
