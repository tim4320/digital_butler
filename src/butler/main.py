import sys
import argparse
from typing import Sequence
# Import our new module
from butler import tidy

def main(argv: Sequence[str] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Digital Butler: Your personal automation tool."
    )

    # Create a sub-command manager
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Command: Tidy ---
    # This adds 'tidy' as a valid command
    tidy_parser = subparsers.add_parser("tidy", help="Organize files in a directory")
    # This adds the --path argument to the tidy command
    tidy_parser.add_argument("--path", required=True, help="The folder to clean up")

    args = parser.parse_args(argv)

    # Router: Decide which function to run based on the command
    if args.command == "tidy":
        tidy.organize_directory(args.path)
    else:
        # If no command is provided, show help
        parser.print_help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
