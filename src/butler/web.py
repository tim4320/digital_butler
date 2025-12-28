import time
import requests
import logging

def check_site(url: str) -> None:
    """
    Pings a website to check availability and response time.
    """
    # Ensure URL has a schema (http/https)
    if not url.startswith("http"):
        url = f"https://{url}"

    logging.info(f"🌍 Pinging {url}...")

    try:
        # Start the timer
        start_time = time.time()

        # Make the request (timeout after 5 seconds so we don't hang forever)
        response = requests.get(url, timeout=5)

        # Stop the timer
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds

        # Analyze the status code
        status_code = response.status_code

        print("\n🌐 --- WEBSITE REPORT --- 🌐")
        print(f"Target:   {url}")

        if 200 <= status_code < 300:
            print(f"Status:   ✅ Online (Code {status_code})")
        elif 400 <= status_code < 500:
            print(f"Status:   ❌ Client Error (Code {status_code})")
        elif 500 <= status_code < 600:
            print(f"Status:   🔥 Server Error (Code {status_code})")
        else:
            print(f"Status:   ⚠️ Unknown (Code {status_code})")

        # Color-code the latency
        if latency < 200:
            speed = "🚀 Fast"
        elif latency < 800:
            speed = "​​​​​🐢 Slow"
        else:
            speed = "🐌 Sluggish"

        print(f"Latency:  {latency:.2f} ms ({speed})")
        print("---------------------------")

    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to {url}. Is the internet down?")
    except requests.exceptions.Timeout:
        print(f"❌ Error: {url} took too long to respond.")
    except Exception as e:
        print(f"❌ Error: Something went wrong: {e}")
