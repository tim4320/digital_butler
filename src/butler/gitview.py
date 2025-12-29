import os
import subprocess
from rich.console import Console
from rich.table import Table

console = Console()

def show_activity(repo_path="."):
    """
    Shows the last 5 git commits in a formatted table.
    """
    try:
        # Verify it is a git repo
        if not os.path.exists(os.path.join(repo_path, ".git")):
            console.print("[bold red]❌ Current folder is not a git repository.[/bold red]")
            return

        # Fetch the log: Hash | Author | Time | Message
        cmd = ["git", "log", "-n", "5", "--pretty=format:%h|%an|%ar|%s"]

        # Run the command safely
        output = subprocess.check_output(cmd, cwd=repo_path).decode("utf-8")

        # Build the Table
        table = Table(title="Recent Git Activity")
        table.add_column("Commit", style="cyan", no_wrap=True)
        table.add_column("Author", style="magenta")
        table.add_column("When", style="green")
        table.add_column("Message", style="white")

        # Populate rows
        for line in output.strip().split("\n"):
            parts = line.split("|")
            if len(parts) >= 4:
                table.add_row(parts[0], parts[1], parts[2], parts[3])

        console.print(table)

    except subprocess.CalledProcessError:
        console.print("[bold red]❌ Error:[/bold red] Could not read git log.")
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
