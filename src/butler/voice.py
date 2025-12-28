import subprocess
from rich.console import Console

console = Console()

def speak(text: str, voice: str = "Samantha") -> None:
    """
    Uses the built-in macOS 'say' command to speak text.
    Voices: Samantha (Siri-like), Fred (Robot), Alex (Classic), Victoria.
    """
    console.print(f"[bold cyan]🗣️  Speaking:[/bold cyan] {text}")

    try:
        # The command we are running is: say -v VoiceName "Text"
        subprocess.run(["say", "-v", voice, text])
    except FileNotFoundError:
        console.print("[red]❌ Error: The 'say' command was not found. Are you on macOS?[/red]")
    except Exception as e:
        console.print(f"[red]❌ Audio Error: {e}[/red]")

def list_voices():
    """Lists available voices on the system."""
    console.print("[yellow]Listing available system voices...[/yellow]")
    subprocess.run(["say", "-v", "?"])
