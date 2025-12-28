import sys
import argparse
import logging
from typing import Sequence

# Imports for our skills
from butler import tidy
from butler import system
from butler import web  # <--- NEW: Import the web module

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

    # --- Command: Tidy ---
    tidy_parser = subparsers.add_parser("tidy", help="Organize files in a directory")
    tidy_parser.add_argument("--path", required=True, help="The folder to clean up")

    # --- Command: Status ---
    subparsers.add_parser("status", help="Show system health (CPU/RAM)")

    # --- Command: Check (Web Watcher) ---
    # <--- NEW: Add the 'check' command
    check_parser = subparsers.add_parser("check", help="Check if a website is online")
    check_parser.add_argument("--url", required=True, help="The website URL (e.g., google.com)")

    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s")

    # Router logic
    if args.command == "tidy":
        tidy.organize_directory(args.path)
    elif args.command == "status":
        system.report_status()
    elif args.command == "check":  # <--- NEW: Route to the web module
        web.check_site(args.url)
    else:
        parser.print_help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
