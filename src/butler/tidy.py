import os
import shutil
from pathlib import Path
from rich.console import Console
from rich.progress import track

console = Console()

def organize_directory(path_str: str) -> None:
    """
    Organizes files into subdirectories based on extensions.
    Now with a progress bar!
    """
    path = Path(path_str)

    if not path.exists():
        console.print(f"[bold red]❌ Error: The path '{path}' does not exist.[/bold red]")
        return

    # 1. Get the list of files first (so we know the total count)
    # We filter out directories and hidden files like .DS_Store
    files = [f for f in path.iterdir() if f.is_file() and not f.name.startswith('.')]

    if not files:
        console.print("[yellow]⚠️  This folder is empty. Nothing to do![/yellow]")
        return

    # Define our rules
    EXTENSIONS = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".heic"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".md", ".csv"],
        "Audio": [".mp3", ".wav", ".aac", ".flac"],
        "Video": [".mp4", ".mov", ".avi", ".mkv"],
        "Archives": [".zip", ".tar", ".gz", ".rar"],
        "Code": [".py", ".js", ".html", ".css", ".json", ".cpp"]
    }

    # 2. The Loop (Wrapped in 'track' for the progress bar)
    # The 'description' text appears next to the bar
    for file in track(files, description="[cyan]🧹 Sweeping up files..."):

        file_extension = file.suffix.lower()
        destination_folder = "Misc"

        # Find the matching category
        for category, exts in EXTENSIONS.items():
            if file_extension in exts:
                destination_folder = category
                break

        # Create the folder if it doesn't exist
        target_dir = path / destination_folder
        target_dir.mkdir(exist_ok=True)

        # Move the file
        try:
            shutil.move(str(file), str(target_dir / file.name))
        except Exception as e:
            console.print(f"[red]Failed to move {file.name}: {e}[/red]")

    console.print(f"[bold green]✨ Done! Organized {len(files)} files.[/bold green]")
