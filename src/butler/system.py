import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout

# Initialize the Rich Console
console = Console()

def report_status() -> None:
    """
    Gather system statistics and print a cyberpunk-style dashboard.
    """
    # Create a loading spinner while we calculate CPU (looks cool)
    with console.status("[bold green]Scanning hardware vitals...", spinner="dots"):
        # 1. Gather Data
        cpu_percent = psutil.cpu_percent(interval=1)

        memory = psutil.virtual_memory()
        total_mem_gb = memory.total / (1024 ** 3)
        used_mem_gb = memory.used / (1024 ** 3)

        disk = psutil.disk_usage('/')
        total_disk_gb = disk.total / (1024 ** 3)
        free_disk_gb = disk.free / (1024 ** 3)

    # 2. Build the CPU/RAM Table
    table = Table(title="System Vital Signs", box=None) # box=None makes it look cleaner

    table.add_column("Component", justify="right", style="cyan", no_wrap=True)
    table.add_column("Usage", style="magenta")
    table.add_column("Details", justify="left", style="green")

    # Add Rows
    # We use a helper function to determine color based on load
    cpu_color = "[green]" if cpu_percent < 50 else "[red]"
    table.add_row(
        "CPU Core",
        f"{cpu_color}{cpu_percent}%",
        _get_bar(cpu_percent)
    )

    mem_color = "[green]" if memory.percent < 70 else "[red]"
    table.add_row(
        "Memory (RAM)",
        f"{mem_color}{memory.percent}%",
        f"{used_mem_gb:.1f}GB / {total_mem_gb:.1f}GB"
    )

    table.add_row(
        "Main Disk",
        f"{disk.percent}%",
        f"{free_disk_gb:.1f}GB Free"
    )

    # 3. Print the Result inside a Panel
    console.print(Panel(table, title="[bold blue]DIGITAL BUTLER v1.0", subtitle="Authorized Access Only"))

def _get_bar(percent, length=20):
    """Simple helper to return a visual bar string"""
    filled = int(length * percent // 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}]"
