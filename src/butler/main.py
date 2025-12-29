import argparse
import sys
# Import ALL modules including payload, ai, and gui
from butler import system, briefing, tasks, netsec, gitview, voice, gui, ai, payload

def main():
    parser = argparse.ArgumentParser(description="Digital Butler - CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- 1. SYSTEM COMMANDS ---
    subparsers.add_parser("tidy", help="Organize Desktop folder")
    subparsers.add_parser("status", help="Show system status")

    # Check (Fixed: No --url flag required anymore)
    check_parser = subparsers.add_parser("check", help="Check security of a URL")
    check_parser.add_argument("target", help="IP or URL to check")

    # News
    news_parser = subparsers.add_parser("news", help="Fetch tech news")
    news_parser.add_argument("--limit", type=int, default=5)
    news_parser.add_argument("--read", action="store_true")
    news_parser.add_argument("--smart", action="store_true")

    # --- 2. MEMORY COMMANDS ---
    subparsers.add_parser("remember", help="Save clipboard")
    subparsers.add_parser("recall", help="Show memory")
    subparsers.add_parser("forget", help="Clear memory")

    # --- 3. TASK COMMANDS ---
    add_parser = subparsers.add_parser("add", help="Add task")
    add_parser.add_argument("task", help="Task text")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--all", action="store_true")

    done_parser = subparsers.add_parser("done", help="Complete task")
    done_parser.add_argument("task_id", type=int)

    # --- 4. NETWORK COMMANDS ---
    scan_parser = subparsers.add_parser("scan", help="Scan an IP")
    scan_parser.add_argument("target", help="Target IP")

    # --- 5. UTILITY COMMANDS ---
    speak_parser = subparsers.add_parser("speak", help="TTS")
    speak_parser.add_argument("text", help="Text to speak")

    subparsers.add_parser("gitview", help="Git activity")

    # Mission Control (This was missing!)
    subparsers.add_parser("mission", help="Launch Dashboard")

    # AI Brain
    ai_parser = subparsers.add_parser("ask", help="Ask AI")
    ai_parser.add_argument("prompt", type=str)

    # Flipper Zero Payloads
    payload_parser = subparsers.add_parser("payload", help="Generate Flipper Scripts")
    payload_sub = payload_parser.add_subparsers(dest="payload_type")

    payload_sub.add_parser("rickroll", help="Generate prank script")

    cmd_parser = payload_sub.add_parser("cmd", help="Generate command script")
    cmd_parser.add_argument("text", type=str)

    wifi_parser = payload_sub.add_parser("wifi", help="Generate Wi-Fi script")
    wifi_parser.add_argument("ssid", help="Network Name")
    wifi_parser.add_argument("password", help="Password")

    args = parser.parse_args()

    # --- ROUTING ---
    if args.command == "tidy": system.organize_desktop()
    elif args.command == "status": system.report_status()
    elif args.command == "check": netsec.check_safety(args.target)
    elif args.command == "news":
        if args.smart: briefing.get_smart_briefing(args.limit, args.read)
        else: briefing.get_top_stories(args.limit, args.read)
    elif args.command == "remember": tasks.remember_clipboard()
    elif args.command == "recall": tasks.recall_memory()
    elif args.command == "forget": tasks.forget_memory()
    elif args.command == "add": tasks.add_task(args.task)
    elif args.command == "list": tasks.list_tasks(args.all)
    elif args.command == "done": tasks.complete_task(args.task_id)
    elif args.command == "scan": netsec.scan_target(args.target)
    elif args.command == "speak": voice.speak(args.text)
    elif args.command == "gitview": gitview.show_activity(".")
    elif args.command == "mission":
        # Launch GUI
        app = gui.DigitalButlerApp()
        app.run()

    # Advanced Modules
    elif args.command == "ask": ai.ask_local_brain(args.prompt)
    elif args.command == "payload":
        if args.payload_type == "rickroll": payload.generate_rickroll()
        elif args.payload_type == "cmd": payload.generate_terminal_command(args.text)
        elif args.payload_type == "wifi": payload.generate_wifi_grabber(args.ssid, args.password)

if __name__ == "__main__":
    main()
