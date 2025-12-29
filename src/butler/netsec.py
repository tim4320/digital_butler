import socket
import ipaddress
import subprocess
import platform
import concurrent.futures
from rich.console import Console

console = Console()

def check_safety(target: str):
    """
    Checks if a URL/IP resolves correctly (basic DNS check).
    """
    clean_target = target.replace("https://", "").replace("http://", "").split("/")[0]
    console.print(f"[bold yellow]🛡️ Checking reputation for:[/bold yellow] {clean_target}")

    try:
        ip = socket.gethostbyname(clean_target)
        console.print(f"[bold green]✅ {clean_target} is reachable at {ip}[/bold green]")
    except socket.gaierror:
        console.print(f"[bold red]❌ Warning:[/bold red] {clean_target} could not be resolved.")

def is_host_up(ip: str) -> bool:
    """
    Pings a host to see if it is alive.
    Works on Mac/Linux/Windows.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Timeout logic: Windows uses -w (ms), Mac/Linux uses -W (sec)
    # We set a short timeout (500ms) to speed up dead hosts
    timeout_arg = ['-W', '500'] if platform.system().lower() == 'windows' else ['-W', '1']

    command = ['ping', param, '1', ip]

    # Mac/Linux ping doesn't support milliseconds easily in all versions,
    # so we rely on the standard 1s timeout or just standard return codes.
    try:
        # Run ping, suppress output
        subprocess.check_call(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False

def scan_target(target: str):
    """
    Scans a CIDR range using threaded Pings (Sonar).
    """
    try:
        if "/" in target:
            network = ipaddress.ip_network(target, strict=False)
            hosts = list(network.hosts())
            total_hosts = len(hosts)

            console.print(f"[bold blue]🔭 Sonar Sweep: {target} ({total_hosts} targets)...[/bold blue]")
            console.print("[dim]Please wait, launching parallel threads...[/dim]")

            active_hosts = []

            # We use a ThreadPool to ping 50 IPs at once
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                # Create a dictionary of {future: ip}
                future_to_ip = {executor.submit(is_host_up, str(ip)): str(ip) for ip in hosts}

                for future in concurrent.futures.as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    try:
                        if future.result():
                            console.print(f"[green]  [+] Device Online: {ip}[/green]")
                            active_hosts.append(ip)
                    except Exception:
                        pass

            console.print(f"[bold green]✅ Scan Complete. Found {len(active_hosts)} active devices.[/bold green]")

        else:
            # Single Target Port Scan (Deep Scan)
            console.print(f"[bold blue]🔬 Deep Scanning: {target}...[/bold blue]")
            common_ports = [21, 22, 53, 80, 443, 445, 3389, 8080]

            for port in common_ports:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((target, port))
                if result == 0:
                    console.print(f"[green]  [+] Port {port} is OPEN[/green]")
                s.close()

    except ValueError:
        console.print("[bold red]❌ Invalid IP or Range format.[/bold red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Scan interrupted by user.[/yellow]")
