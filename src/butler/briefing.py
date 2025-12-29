# src/butler/briefing.py
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from butler import voice, ai  # <--- Import the Brain

console = Console()

def get_smart_briefing(limit: int = 5, read_aloud: bool = False):
    url = "https://news.ycombinator.com/"

    with console.status("[bold purple]Reading the news & thinking..."):
        try:
            # 1. Fetch the raw data
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            story_spans = soup.select(".titleline > a")[:limit]

            # 2. Extract just the text
            headlines = [story.get_text() for story in story_spans]
            headlines_text = "\n".join(headlines)

            # 3. The "Prompt Engineering"
            prompt = (
                f"Here are the top tech headlines:\n{headlines_text}\n\n"
                "Summarize these into a short, 3-sentence briefing for your boss, Timothy. "
                "Be professional but slightly witty. Do not list them, just summarize the vibe."
            )

            # 4. Ask the Local Brain (We need a helper in ai.py that returns string, not prints)
            # We will assume you update ai.py to return the text (see below)
            summary = ai.generate_text(prompt)

            # 5. Display
            console.print(Panel(Markdown(summary), title="🧠 AI INTELLIGENCE REPORT", border_style="purple"))

            # 6. Speak
            if read_aloud:
                voice.speak(summary)

        except Exception as e:
            console.print(f"[bold red]❌ Error:[/bold red] {e}")
