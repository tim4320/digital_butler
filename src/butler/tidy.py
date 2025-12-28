import shutil
import logging # <--- NEW
from pathlib import Path
from typing import Dict, List

# (Keep your EXTENSION_MAP here...)
EXTENSION_MAP: Dict[str, List[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".heic"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"]
}

def organize_directory(directory_path: str) -> None:
    path = Path(directory_path)

    if not path.exists():
        # ERROR level for actual problems
        logging.error(f"❌ Error: The path '{directory_path}' does not exist.")
        return

    # INFO level for standard feedback
    logging.info(f"📦 Organizing: {path.resolve()}")

    for item in path.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            _move_file(item, path)

def _move_file(file_path: Path, root_path: Path) -> None:
    extension = file_path.suffix.lower()
    destination_folder_name = "Misc"

    for folder_name, extensions in EXTENSION_MAP.items():
        if extension in extensions:
            destination_folder_name = folder_name
            break

    target_folder = root_path / destination_folder_name
    target_folder.mkdir(exist_ok=True)

    destination_file = target_folder / file_path.name

    # DEBUG level: The user doesn't need to see every single file move
    # unless they are troubleshooting.
    logging.debug(f"   -> Moving {file_path.name} to {destination_folder_name}/")

    shutil.move(str(file_path), str(destination_file))
