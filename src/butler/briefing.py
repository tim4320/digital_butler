import requests
from bs4 import BeautifulSoup
import logging

def get_top_stories(limit: int = 5) -> None:
    """
    Fetches the top stories from Hacker News.
    """
    url = "https://news.ycombinator.com/"

    logging.info(f"📰 Fetching daily briefing from {url}...")

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"❌ Error: Could not fetch news (Status {response.status_code})")
            return

        # Parse the HTML
        # 'html.parser' is built-in to Python, so no extra install needed for the parser engine
        soup = BeautifulSoup(response.text, "html.parser")

        # --- THE HARD PART (Finding the data) ---
        # On Hacker News, titles are in a <span> with class "titleline"
        # We use CSS selectors to find them.
        story_spans = soup.select(".titleline > a")

        print(f"\n☕ --- DAILY BRIEFING ({limit} Stories) --- ☕")

        # Loop through and print the first 'limit' items
        for i, story in enumerate(story_spans[:limit], 1):
            title = story.get_text()
            raw_link = story['href'] # <--- Get the raw link first

            # --- THE FIX ---
            if raw_link.startswith("http"):
                link = raw_link
            else:
                # It's an internal link, prepend the domain
                link = f"https://news.ycombinator.com/{raw_link}"
            # ----------------

            print(f"{i}. {title}")
            print(f"   🔗 {link}")
            print("")

    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        print("❌ Error: Could not read the news today.")
