import socket
from rich.console import Console
from rich.table import Table

console = Console()

def scan_target(target_ip: str):
    """
    Scans a target IP for common open ports.
    """
    # The most common ports hackers/admins look for
    PORTS_TO_SCAN = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        53: "DNS",
        80: "HTTP",
        443: "HTTPS",
        3306: "MySQL",
        8080: "Web Proxy"
    }

    console.print(f"[bold blue]🔭 Scanning target: {target_ip}[/bold blue]")

    table = Table(title=f"Port Scan Results: {target_ip}")
    table.add_column("Port", justify="right", style="cyan")
    table.add_column("Service", style="white")
    table.add_column("Status", justify="center")

    # Set a default timeout so we don't wait forever on closed ports
    socket.setdefaulttimeout(0.5)

    for port, service in PORTS_TO_SCAN.items():
        # Create a new socket for each check
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # The .connect_ex() method returns 0 if successful (Open)
        result = s.connect_ex((target_ip, port))

        if result == 0:
            status = "[bold green]OPEN[/bold green]"
            icon = "🔓"
        else:
            status = "[dim red]CLOSED[/dim red]"
            icon = "🔒"

        table.add_row(str(port), service, f"{icon} {status}")
        s.close()

    console.print(table)
