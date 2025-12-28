import subprocess
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def get_git_history(limit: int = 10):
    """
    Fetches the git log and renders it as a dashboard.
    """
    try:
        # 1. Run the git command
        # We use a custom format: Hash|Author|Time|Message
        # %h = short hash, %an = author name, %ar = relative date, %s = subject
        cmd = [
            "git", "log",
            f"-n {limit}",
            "--pretty=format:%h|%an|%ar|%s"
        ]

        # Capture the output
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        output = result.decode("utf-8").strip()

    except subprocess.CalledProcessError:
        console.print("[bold red]❌ Error: Not a valid git repository (or git is missing).[/bold red]")
        return
    except FileNotFoundError:
        console.print("[bold red]❌ Error: Git is not installed on this system.[/bold red]")
        return

    if not output:
        console.print("[yellow]⚠️  No commit history found.[/yellow]")
        return

    # 2. Build the UI
    table = Table(title="📜 Project Timeline", box=None)

    table.add_column("Hash", style="cyan", no_wrap=True)
    table.add_column("When", style="green")
    table.add_column("Author", style="blue")
    table.add_column("Message", style="white bold")

    # 3. Parse the data
    # We split the raw text block into lines, then split lines by "|"
    lines = output.split("\n")

    for line in lines:
        try:
            # We split only 3 times to avoid breaking messages that contain pipes
            short_hash, author, date, message = line.split("|", 3)

            # Add to table
            table.add_row(short_hash, date, author, message)
        except ValueError:
            continue

    # 4. Show it
    console.print(Panel(table, border_style="cyan"))
