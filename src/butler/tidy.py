import shutil
from pathlib import Path
from typing import Dict, List

# Configuration: Which extensions go where?
# We use a constant (UPPER_CASE) because this doesn't change during runtime.
EXTENSION_MAP: Dict[str, List[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".heic"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"]
}

def organize_directory(directory_path: str) -> None:
    """
    Scans the directory and moves files into categorized subfolders.
    """
    # Convert string to a Path object. This is the 'pathlib' magic.
    path = Path(directory_path)

    if not path.exists():
        print(f"❌ Error: The path '{directory_path}' does not exist.")
        return

    print(f"📦 Organizing: {path.resolve()}")

    # Iterate over every item in this directory
    for item in path.iterdir():
        # Safety check: We only move files, not folders (to avoid infinite loops)
        # and we don't move hidden files (starting with .)
        if item.is_file() and not item.name.startswith('.'):
            _move_file(item, path)

def _move_file(file_path: Path, root_path: Path) -> None:
    """
    Internal helper function to determine destination and move the file.
    Note the underscore (_move_file): Convention for 'internal use only'.
    """
    extension = file_path.suffix.lower()

    # Default destination if no match found
    destination_folder_name = "Misc"

    # Check our map to find the right folder
    for folder_name, extensions in EXTENSION_MAP.items():
        if extension in extensions:
            destination_folder_name = folder_name
            break

    # Create the destination folder object
    target_folder = root_path / destination_folder_name

    # Actually create the folder on the disk if it doesn't exist
    target_folder.mkdir(exist_ok=True)

    # Move the file
    destination_file = target_folder / file_path.name
    print(f"   -> Moving {file_path.name} to {destination_folder_name}/")
    shutil.move(str(file_path), str(destination_file))
