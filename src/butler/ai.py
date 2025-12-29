import requests
import json
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

def ask_local_brain(prompt: str, model: str = "llama3.2"):
    """
    Sends a prompt to the local Ollama instance and prints the response.
    """
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # Set to True if you want the "typing" effect later
    }

    console.print(f"[bold green]🧠 Neural Engine is thinking ({model})...[/bold green]")

    try:
        # Send the request to your local machine
        response = requests.post(url, json=payload, timeout=60)

        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "")

            # Render the answer as beautiful Markdown
            md = Markdown(answer)
            console.print(Panel(md, title="🤖 LOCAL AI RESPONSE", border_style="purple"))

            # Log usage stats (optional flex)
            duration = data.get("total_duration", 0) / 1e9  # convert nanoseconds to seconds
            console.print(f"[dim]Generated in {duration:.2f} seconds on Apple M4[/dim]")

        else:
            console.print(f"[bold red]❌ Error: Ollama returned {response.status_code}[/bold red]")

    except requests.exceptions.ConnectionError:
        console.print("[bold red]❌ Error: Could not connect to Ollama.[/bold red]")
        console.print("[yellow]Make sure the Ollama app is running in the background![/yellow]")

    def generate_text(prompt: str, model: str = "llama3.2") -> str:

     """ Returns the raw string response from Ollama (for internal use).
    """
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}

    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "")
    except:
        return "I am unable to process the data right now, sir."
    return "Error contacting Neural Engine."
