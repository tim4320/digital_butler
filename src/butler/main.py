import sys
import argparse
import logging
from typing import Sequence

# --- IMPORTS FOR ALL SKILLS ---
from butler import tidy
from butler import system
from butler import web
from butler import briefing
from butler import brain
from butler import tasks   # Option A: Database
from butler import netsec  # Option B: Port Scanner
from butler import voice   # Option C: Text-to-Speech

def main(argv: Sequence[str] = None) -> int:
    # 1. Initialize the Database immediately
    # This ensures the .db file exists before we try to use it
    tasks.init_db()

    # 2. Setup the Argument Parser
    parser = argparse.ArgumentParser(
        description="Digital Butler: Your personal automation tool."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed debug information"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- COMMANDS ---

    # 1. Tidy (File Organizer)
    tidy_parser = subparsers.add_parser("tidy", help="Organize files")
    tidy_parser.add_argument("--path", required=True, help="The folder to clean up")

    # 2. Status (System Monitor)
    subparsers.add_parser("status", help="Show system health")

    # 3. Check (Website Pinger)
    check_parser = subparsers.add_parser("check", help="Check website status")
    check_parser.add_argument("--url", required=True, help="URL to ping")

    # 4. News (Hacker News Scraper)
    news_parser = subparsers.add_parser("news", help="Get top headlines")
    news_parser.add_argument("--limit", type=int, default=5, help="How many stories")
    # NEW FLAG
    news_parser.add_argument("--read", action="store_true", help="Read stories out loud")

    # 5. Memory (JSON Brain)
    rem_parser = subparsers.add_parser("remember", help="Save a fact")
    rem_parser.add_argument("key", help="What to remember")
    rem_parser.add_argument("value", help="The content")

    rec_parser = subparsers.add_parser("recall", help="Retrieve facts")
    rec_parser.add_argument("key", nargs='?', help="Specific fact to look up")

    for_parser = subparsers.add_parser("forget", help="Delete a fact")
    for_parser.add_argument("key", help="Fact to delete")

    # 6. Tasks (SQLite Database) - NEW
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="The task description")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--all", action="store_true", help="Show completed tasks too")

    done_parser = subparsers.add_parser("done", help="Complete a task")
    done_parser.add_argument("id", type=int, help="The ID of the task to finish")

    # 7. NetSec (Port Scanner) - NEW
    scan_parser = subparsers.add_parser("scan", help="Scan network ports")
    scan_parser.add_argument("target", help="IP address or Domain")

    # 8. Voice (Text-to-Speech) - NEW
    speak_parser = subparsers.add_parser("speak", help="Text-to-Speech")
    speak_parser.add_argument("text", help="What to say")
    speak_parser.add_argument("--voice", default="Samantha", help="Voice name (e.g. Fred, Alex)")

    # --- PARSING ---
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s")

    # --- ROUTING (The Switchboard) ---
    if args.command == "tidy":
        tidy.organize_directory(args.path)
    elif args.command == "status":
        system.report_status()
    elif args.command == "check":
        web.check_site(args.url)
    elif args.command == "news":
        briefing.get_top_stories(args.limit, args.read) # Pass the new flag
    elif args.command == "speak":
        voice.speak(args.text, args.voice)

    # Memory Routing
    elif args.command == "remember":
        brain.remember(args.key, args.value)
    elif args.command == "recall":
        brain.recall(args.key)
    elif args.command == "forget":
        brain.forget(args.key)

    # Task Routing (Database)
    elif args.command == "add":
        tasks.add_task(args.description)
    elif args.command == "list":
        tasks.list_tasks(args.all)
    elif args.command == "done":
        tasks.complete_task(args.id)

    # NetSec Routing (Scanner)
    elif args.command == "scan":
        netsec.scan_target(args.target)

    else:
        parser.print_help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
