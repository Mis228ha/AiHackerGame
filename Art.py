"""
art.py — ASCII-баннер и все визуальные арт-блоки игры.
"""

import random
import time
from Colors import BRIGHT_GREEN, DIM_GREEN, GREEN, RED, YELLOW, CYAN, RESET, BLINK
from Colors import slow_print, scan_line, r, g, y, dim

# ─── ГЛАВНЫЙ БАННЕР ──────────────────────────────────────────────────────────

BANNER = f"""
{BRIGHT_GREEN}
  ██████╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗ ██████╗ ██████╗ ███████╗
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║     ██║   ██║██████╔╝█████╗  
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║     ██║   ██║██╔══██╗██╔══╝  
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║╚██████╗╚██████╔╝██║  ██║███████╗
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
{RESET}{DIM_GREEN}
                    ██████╗ ██████╗ ███████╗ █████╗  ██████╗██╗  ██╗
                    ██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║
                    ██████╔╝██████╔╝█████╗  ███████║██║     ███████║
                    ██╔══██╗██╔══██╗██╔══╝  ██╔══██║██║     ██╔══██║
                    ██████╔╝██║  ██║███████╗██║  ██║╚██████╗██║  ██║
                    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
{RESET}
{DIM_GREEN}                         [ PROTOCOL v2.4.1 — UNAUTHORIZED ACCESS ]
                    [ PSYCHO-ADAPTIVE AI DEFENSE SYSTEM ACTIVE ]
{RESET}"""


# ─── АРТ: КОНЦОВКИ ───────────────────────────────────────────────────────────

def art_true_breach():
    """Печатает ASCII-арт надписи TRUE BREACH."""
    slow_print(f"{BRIGHT_GREEN}  ████████╗██████╗ ██╗   ██╗███████╗{RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██╔══╝██╔══██╗██║   ██║██╔════╝{RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██║   ██████╔╝██║   ██║█████╗  {RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██║   ██╔══██╗██║   ██║██╔══╝  {RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██║   ██║  ██║╚██████╔╝███████╗{RESET}")
    slow_print(f"{BRIGHT_GREEN}     ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝  BREACH{RESET}")


def art_trace_caught():
    """Печатает ASCII-арт надписи CAUGHT."""
    slow_print(f"{RED}  ██████╗  █████╗ ██╗   ██╗ ██████╗ ██╗  ██╗████████╗{RESET}", 0.01)
    slow_print(f"{RED}  ██╔════╝██╔══██╗██║   ██║██╔════╝ ██║  ██║╚══██╔══╝{RESET}", 0.01)
    slow_print(f"{RED}  ██║     ███████║██║   ██║██║  ███╗███████║   ██║{RESET}", 0.01)
    slow_print(f"{RED}  ██║     ██╔══██║██║   ██║██║   ██║██╔══██║   ██║{RESET}", 0.01)
    slow_print(f"{RED}  ╚██████╗██║  ██║╚██████╔╝╚██████╔╝██║  ██║   ██║{RESET}", 0.01)
    slow_print(f"{RED}   ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝{RESET}", 0.01)


def art_iamroot():
    """Печатает ASCII-арт чит-кода IAMROOT (ROOT)."""
    print(f"{BRIGHT_GREEN}  ██████╗  ██████╗  ██████╗ ████████╗{RESET}")
    print(f"{BRIGHT_GREEN}  ██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝{RESET}")
    print(f"{BRIGHT_GREEN}  ██████╔╝██║   ██║██║   ██║   ██║{RESET}")
    print(f"{BRIGHT_GREEN}  ██╔══██╗██║   ██║██║   ██║   ██║{RESET}")
    print(f"{BRIGHT_GREEN}  ██║  ██║╚██████╔╝╚██████╔╝   ██║{RESET}")
    print(f"{BRIGHT_GREEN}  ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝{RESET}")


def art_godmode():
    """Печатает ASCII-арт чит-кода GODMODE."""
    print(f"{BRIGHT_GREEN}  ██████╗  ██████╗ ██████╗{RESET}")
    print(f"{BRIGHT_GREEN}  ██╔════╝██╔═══██╗██╔══██╗{RESET}")
    print(f"{BRIGHT_GREEN}  ██║  ███╗██║   ██║██║  ██║{RESET}")
    print(f"{BRIGHT_GREEN}  ██║   ██║██║   ██║██║  ██║{RESET}")
    print(f"{BRIGHT_GREEN}  ╚██████╔╝╚██████╔╝██████╔╝{RESET}")
    print(f"{BRIGHT_GREEN}  ╚═════╝  ╚═════╝ ╚═════╝   MODE: ON{RESET}")


def art_matrix():
    """Анимация пасхалки MATRIX."""
    print()
    chars = "01アイウエオカキクケコ@#$%&*<>[]{}|"
    for _ in range(6):
        line = "  "
        for _ in range(58):
            line += random.choice(chars)
        print(f"{DIM_GREEN}{line}{RESET}")
        time.sleep(0.07)
    print()
    slow_print(f"{BRIGHT_GREEN}  Wake up, hacker...{RESET}", delay=0.05)
    slow_print(f"{BRIGHT_GREEN}  The Matrix has you.{RESET}", delay=0.05)
    slow_print(f"{GREEN}  Follow the white rabbit.{RESET}", delay=0.05)


# ─── СЛУЧАЙНЫЕ СОБЫТИЯ (атмосферные строки) ──────────────────────────────────

LOCAL_EVENTS = [
    f"{BLINK}{RED}⚠  WARNING: UNAUTHORIZED ACCESS DETECTED{RESET}",
    f"{RED}◈  TRACE ROUTING INITIATED... NODE 7 → NODE 23 → NODE 44{RESET}",
    f"{YELLOW}◉  FIREWALL RECONFIGURING... LAYER 3 HARDENED{RESET}",
    f"{RED}◈  SYSTEM IS WATCHING YOU. BEHAVIORAL LOG UPDATED.{RESET}",
    f"{YELLOW}◉  INTRUSION COUNTERMEASURE ENGAGED{RESET}",
    f"{RED}◈  ENCRYPTED CHANNEL COMPROMISED — REROUTING{RESET}",
]