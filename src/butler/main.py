import sys
import argparse
import logging
from typing import Sequence
# Import BOTH modules now
from butler import tidy
from butler import system  # <--- NEW

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

    # --- Command: Status (NEW) ---
    # No arguments needed for this one!
    subparsers.add_parser("status", help="Show system health (CPU/RAM)")

    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s")

    # Router
    if args.command == "tidy":
        tidy.organize_directory(args.path)
    elif args.command == "status":  # <--- NEW
        system.report_status()
    else:
        parser.print_help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
