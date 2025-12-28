import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from butler import voice  # <--- Link to the Voice Module

console = Console()

def get_top_stories(limit: int = 5, read_aloud: bool = False) -> None:
    url = "https://news.ycombinator.com/"

    with console.status("[bold yellow]Fetching intelligence from the web..."):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                console.print(f"[bold red]❌ Error: HTTP {response.status_code}")
                return

            soup = BeautifulSoup(response.text, "html.parser")
            story_spans = soup.select(".titleline > a")

            md_content = ""

            # If reading aloud, give an intro
            if read_aloud:
                voice.speak(f"Here are the top {limit} stories for today.")

            for i, story in enumerate(story_spans[:limit], 1):
                title = story.get_text()
                raw_link = story['href']

                # Fix relative URLs
                if raw_link.startswith("http"):
                    link = raw_link
                else:
                    link = f"https://news.ycombinator.com/{raw_link}"

                md_content += f"**{i}. {title}**\n"
                md_content += f"[link={link}]🔗 Click to Open[/link]\n\n"

                # --- THE INTEGRATION ---
                if read_aloud:
                    # Speak just the title
                    voice.speak(f"Story {i}: {title}")
                # -----------------------

            md = Markdown(md_content)
            console.print(Panel(md, title="📰 DAILY BRIEFING", border_style="yellow"))

        except Exception as e:
            console.print(f"[bold red]❌ Critical Failure:[/bold red] {e}")
