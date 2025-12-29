from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Button, Static, Label, Markdown
from butler import system, briefing, tasks, netsec
from rich.text import Text

# We need to capture the output of our functions,
# so we will redirect print() to a variable for the GUI.
import io
import sys
from rich.console import Console

class DigitalButlerApp(App):
    """The TUI (Terminal User Interface) for Digital Butler."""

    CSS = """
    Screen {
        layout: vertical;
    }
    #sidebar {
        width: 30;
        background: $panel;
        dock: left;
        height: 100%;
        border-right: heavy $accent;
    }
    #output_window {
        height: 100%;
        background: $background;
        padding: 1 2;
        border: solid green;
    }
    Button {
        width: 100%;
        margin-bottom: 1;
    }
    .title {
        text-align: center;
        padding: 1;
        background: $accent;
        color: $text;
        text-style: bold;
        margin-bottom: 2;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)

        # Main Layout
        with Container():
            # Left Sidebar with Buttons
            with Container(id="sidebar"):
                yield Label("COMMAND DECK", classes="title")
                yield Button("🖥️  System Status", id="btn_status", variant="primary")
                yield Button("📰  Fetch News", id="btn_news", variant="warning")
                yield Button("📝  List Tasks", id="btn_tasks", variant="success")
                yield Button("🔭  Scan Router", id="btn_scan", variant="error")
                yield Button("EXIT", id="btn_exit")

            # Right Area for Output
            with VerticalScroll(id="output_window"):
                yield Static("Waiting for command...", id="output_log")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        button_id = event.button.id

        if button_id == "btn_exit":
            self.exit()

        elif button_id == "btn_status":
            self.run_and_display(system.report_status)

        elif button_id == "btn_news":
            # We wrap the news function to pass arguments
            self.run_and_display(lambda: briefing.get_top_stories(limit=3))

        elif button_id == "btn_tasks":
            self.run_and_display(lambda: tasks.list_tasks(show_all=True))

        elif button_id == "btn_scan":
            self.update_output("Scanning local network... (This may take a moment)")
            # In a real app, we'd run this in a thread to not freeze the UI
            # For now, we just run it directly
            self.run_and_display(lambda: netsec.scan_target("192.168.1.1"))

    def run_and_display(self, func):
        """Helper to capture print() output and show it in the UI."""

        # 1. Capture stdout
        capture = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = capture

        # 2. Run the function
        # We also need to tell Rich to print to this new string, not the real terminal
        try:
            # Temporarily redirect Rich console output if possible,
            # but for now capturing stdout handles the raw print.
            # (Rich keeps its own console instance, so this is a simplified hack)
            func()
        except Exception as e:
            print(f"Error: {e}")

        # 3. Restore stdout
        sys.stdout = old_stdout

        # 4. Update the UI
        # We convert the raw ANSI codes into a safe Rich Text object
        result_text = Text.from_ansi(capture.getvalue())

        self.update_output(result_text)
        
    def update_output(self, text: str):
        """Updates the text in the main window."""
        log_widget = self.query_one("#output_log", Static)
        log_widget.update(text)

if __name__ == "__main__":
    app = DigitalButlerApp()
    app.run()
