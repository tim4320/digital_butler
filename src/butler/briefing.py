import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from butler import voice, ai

console = Console()

# --- 1. THE CLASSIC FUNCTION (Fixes your error) ---
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

            if read_aloud:
                voice.speak(f"Here are the top {limit} stories for today.")

            for i, story in enumerate(story_spans[:limit], 1):
                title = story.get_text()
                raw_link = story['href']

                if raw_link.startswith("http"):
                    link = raw_link
                else:
                    link = f"https://news.ycombinator.com/{raw_link}"

                md_content += f"**{i}. {title}**\n"
                md_content += f"[link={link}]🔗 Click to Open[/link]\n\n"

                if read_aloud:
                    voice.speak(f"Story {i}: {title}")

            md = Markdown(md_content)
            console.print(Panel(md, title="📰 DAILY BRIEFING", border_style="yellow"))

        except Exception as e:
            console.print(f"[bold red]❌ Critical Failure:[/bold red] {e}")

# --- 2. THE NEW AI FUNCTION (For the "Smart" flag) ---
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

            # 4. Ask the Local Brain
            summary = ai.generate_text(prompt)

            # 5. Display
            console.print(Panel(Markdown(summary), title="🧠 AI INTELLIGENCE REPORT", border_style="purple"))

            # 6. Speak
            if read_aloud:
                voice.speak(summary)

        except Exception as e:
            console.print(f"[bold red]❌ Error:[/bold red] {e}")
