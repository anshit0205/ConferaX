# thinking_indicators.py
# Real-time thinking indicators and progress display for ConferaX

import time
import sys
import threading


class ThinkingIndicator:
    """
    Displays a live thinking animation while an agent is processing.
    Shows phase name, agent name, and elapsed time.
    """

    SPINNER = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    COLORS = {
        "blue": "\033[94m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "white": "\033[97m",
        "bold": "\033[1m",
        "reset": "\033[0m",
    }

    def __init__(self, agent_name: str, phase: str, color: str = "cyan"):
        self.agent_name = agent_name
        self.phase = phase
        self.color = color
        self._running = False
        self._thread = None
        self._start_time = None

    def _animate(self):
        i = 0
        while self._running:
            elapsed = time.time() - self._start_time
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            time_str = f"{mins:02d}:{secs:02d}"
            spinner = self.SPINNER[i % len(self.SPINNER)]
            c = self.COLORS.get(self.color, "")
            bold = self.COLORS["bold"]
            reset = self.COLORS["reset"]
            line = f"\r  {c}{spinner}{reset} {bold}{self.phase}{reset}  {c}{self.agent_name}{reset} is thinking...  [{time_str}]   "
            sys.stdout.write(line)
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def start(self):
        self._running = True
        self._start_time = time.time()
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def stop(self, success: bool = True):
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.5)
        elapsed = time.time() - self._start_time
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        icon = "✅" if success else "❌"
        c = self.COLORS.get("green" if success else "red", "")
        bold = self.COLORS["bold"]
        reset = self.COLORS["reset"]
        print(f"\r  {icon} {bold}{self.phase}{reset}  {c}{self.agent_name}{reset} complete  [{mins:02d}:{secs:02d}]          ")


def print_phase_header(phase_num: int, phase_name: str, description: str = ""):
    """Prints a styled phase header."""
    colors = {1: "blue", 2: "cyan", 3: "yellow", 4: "magenta", 5: "green", 6: "red", 7: "cyan", 8: "green"}
    color_map = {
        "blue": "\033[94m", "cyan": "\033[96m", "yellow": "\033[93m",
        "magenta": "\033[95m", "green": "\033[92m", "red": "\033[91m",
    }
    color_code = color_map.get(colors.get(phase_num, "cyan"), "\033[96m")
    bold = "\033[1m"
    reset = "\033[0m"
    width = 62
    print(f"\n{color_code}{'─' * width}{reset}")
    print(f"{color_code}{bold}  PHASE {phase_num}: {phase_name.upper()}{reset}")
    if description:
        print(f"  {description}")
    print(f"{color_code}{'─' * width}{reset}")


def print_agent_start(agent_name: str, mission: str):
    """Shows what an agent is about to do."""
    cyan = "\033[96m"
    bold = "\033[1m"
    reset = "\033[0m"
    print(f"\n  {cyan}▶{reset} {bold}{agent_name}{reset}")
    print(f"    Mission: {mission}")


def print_agent_result(agent_name: str, result_preview: str = ""):
    """Shows agent completed with a result preview."""
    green = "\033[92m"
    bold = "\033[1m"
    reset = "\033[0m"
    preview = result_preview[:120] + "..." if len(result_preview) > 120 else result_preview
    print(f"\n  {green}✓{reset} {bold}{agent_name}{reset} delivered output")
    if preview:
        print(f"    Preview: {preview}")


def print_conferax_banner():
    """Prints the ConferaX startup banner."""
    bold = "\033[1m"
    cyan = "\033[96m"
    blue = "\033[94m"
    reset = "\033[0m"
    banner = f"""
{cyan}{bold}
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║   🧠  ConferaX — Autonomous Conference Intelligence     ║
  ║        SOTA Multi-Agent Decision Engine v2.0             ║
  ║                                                          ║
  ║   Agents: 14  |  Phases: 12  |  Decision Layer: Active   ║
  ║   Devil's Advocate: ON  |  Self-Reflection: ON           ║
  ║   Real-Time Research: ON  |  Live Indicators: ON         ║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝
{reset}"""
    print(banner)


def print_decision_callout(decision_num: int, decision: str, confidence: int):
    """Highlights a final decision made by the Decision Layer."""
    yellow = "\033[93m"
    bold = "\033[1m"
    green = "\033[92m"
    red = "\033[91m"
    reset = "\033[0m"
    conf_color = green if confidence >= 70 else (yellow if confidence >= 50 else red)
    print(f"\n  {yellow}◆{reset} {bold}DECISION {decision_num}{reset}: {decision}")
    print(f"    Confidence: {conf_color}{bold}{confidence}/100{reset}")


def print_completion_summary(phases_completed: int, total_time: float, output_path: str):
    """Final completion banner."""
    green = "\033[92m"
    bold = "\033[1m"
    cyan = "\033[96m"
    reset = "\033[0m"
    mins = int(total_time // 60)
    secs = int(total_time % 60)
    print(f"""
{green}{bold}
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║   🎉  ConferaX Complete!                                ║
  ║                                                          ║
  ║   Phases completed : {phases_completed}/12                              ║
  ║   Total time       : {mins:02d}m {secs:02d}s                            ║
  ║   Output           : conferax_report.html                ║
  ║                                                          ║
  ║   Open the HTML report in your browser.                  ║
  ║   Your conference strategy is ready.                     ║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝
{reset}""")
