import sqlite3
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()
DB_FILE = Path.home() / ".butler_data.db"

def _get_connection():
    """Connects to the database (creates it if missing)."""
    conn = sqlite3.connect(DB_FILE)
    # This line makes the rows look like dictionaries instead of tuples
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the table structure if it doesn't exist."""
    conn = _get_connection()
    cursor = conn.cursor()

    # SQL: Create a table with an ID, a Description, and a Status
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

def add_task(description: str):
    """Adds a new row to the table."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO todos (task) VALUES (?)", (description,))
    conn.commit()
    conn.close()

    console.print(f"[bold green]✅ Added task:[/bold green] {description}")

def list_tasks(show_all=False):
    """Reads rows and displays them in a Rich Table."""
    conn = _get_connection()
    cursor = conn.cursor()

    if show_all:
        query = "SELECT * FROM todos"
    else:
        query = "SELECT * FROM todos WHERE status = 'pending'"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]Nothing to do! Relax. 🏖️[/yellow]")
        return

    # Build the UI Table
    table = Table(title="Task List")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Task", style="white")
    table.add_column("Status", justify="center")

    for row in rows:
        status_style = "green" if row['status'] == 'done' else "red"
        status_icon = "✅" if row['status'] == 'done' else "⏳"

        table.add_row(
            str(row['id']),
            row['task'],
            f"[{status_style}]{status_icon} {row['status']}"
        )

    console.print(table)

def complete_task(task_id: int):
    """Updates a row to set status to 'done'."""
    conn = _get_connection()
    cursor = conn.cursor()

    # Check if it exists first
    cursor.execute("SELECT * FROM todos WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        console.print(f"[red]❌ Task ID {task_id} not found.[/red]")
        return

    # The Update
    cursor.execute("UPDATE todos SET status = 'done' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    console.print(f"[bold green]✨ Task {task_id} marked as complete![/bold green]")
