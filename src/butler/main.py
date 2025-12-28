import sys
import argparse
import logging
from typing import Sequence

# Imports for ALL our skills
from butler import tidy
from butler import system
from butler import web
from butler import briefing
from butler import brain   # <--- NEW: Import the brain

def main(argv: Sequence[str] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Digital Butler: Your personal automation tool."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed debug information"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Existing Commands ---
    tidy_parser = subparsers.add_parser("tidy", help="Organize files")
    tidy_parser.add_argument("--path", required=True, help="The folder to clean up")

    subparsers.add_parser("status", help="Show system health")

    check_parser = subparsers.add_parser("check", help="Check website status")
    check_parser.add_argument("--url", required=True, help="URL to ping")

    news_parser = subparsers.add_parser("news", help="Get top headlines")
    news_parser.add_argument("--limit", type=int, default=5, help="How many stories")

    # --- NEW: Memory Commands ---

    # 1. REMEMBER: Needs a Key and a Value
    rem_parser = subparsers.add_parser("remember", help="Save a fact")
    rem_parser.add_argument("key", help="What to remember (e.g. 'wifi')")
    rem_parser.add_argument("value", help="The content (e.g. 'secret123')")

    # 2. RECALL: Key is Optional
    rec_parser = subparsers.add_parser("recall", help="Retrieve facts")
    # nargs='?' means "zero or one argument". If zero, it's None.
    rec_parser.add_argument("key", nargs='?', help="Specific fact to look up")

    # 3. FORGET: Key is Required
    for_parser = subparsers.add_parser("forget", help="Delete a fact")
    for_parser.add_argument("key", help="Fact to delete")


    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s")

    # --- Router ---
    if args.command == "tidy":
        tidy.organize_directory(args.path)
    elif args.command == "status":
        system.report_status()
    elif args.command == "check":
        web.check_site(args.url)
    elif args.command == "news":
        briefing.get_top_stories(args.limit)

    # --- NEW: Routing for Brain ---
    elif args.command == "remember":
        brain.remember(args.key, args.value)
    elif args.command == "recall":
        brain.recall(args.key)
    elif args.command == "forget":
        brain.forget(args.key)

    else:
        parser.print_help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
