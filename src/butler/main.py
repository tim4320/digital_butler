import sys
import argparse
import logging  # <--- NEW
from typing import Sequence
from butler import tidy

def main(argv: Sequence[str] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Digital Butler: Your personal automation tool."
    )

    # <--- NEW: Add a verbose flag (global option)
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed debug information"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Command: Tidy ---
    tidy_parser = subparsers.add_parser("tidy", help="Organize files in a directory")
    tidy_parser.add_argument("--path", required=True, help="The folder to clean up")

    args = parser.parse_args(argv)

    # <--- NEW: Configure the Logger based on the flag
    log_level = logging.DEBUG if args.verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(message)s", # Simple format for now
        # format="%(asctime)s - %(levelname)s - %(message)s", # Pro format (try this later)
    )

    # We use logging.debug for stuff only developers care about
    logging.debug(f"🔧 Debug Mode Enabled. Arguments: {args}")

    if args.command == "tidy":
        tidy.organize_directory(args.path)
    else:
        parser.print_help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
