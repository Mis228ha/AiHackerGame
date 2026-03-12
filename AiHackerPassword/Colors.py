"""
Colors.py — ANSI-цвета, утилиты вывода и разделительные линии.
"""

import time

# ─── ANSI ЦВЕТА ───────────────────────────────────────────────────────────────

GREEN        = "\033[92m"
BRIGHT_GREEN = "\033[1;92m"
DIM_GREEN    = "\033[2;32m"
RED          = "\033[91m"
YELLOW       = "\033[93m"
CYAN         = "\033[96m"
WHITE        = "\033[97m"
DIM          = "\033[2m"
BOLD         = "\033[1m"
BLINK        = "\033[5m"
RESET        = "\033[0m"


def g(text):   return f"{GREEN}{text}{RESET}"
def bg(text):  return f"{BRIGHT_GREEN}{text}{RESET}"
def r(text):   return f"{RED}{text}{RESET}"
def y(text):   return f"{YELLOW}{text}{RESET}"
def c(text):   return f"{CYAN}{text}{RESET}"
def dim(text): return f"{DIM_GREEN}{text}{RESET}"


def slow_print(text, delay=0.006):
    """Посимвольная печать с задержкой."""
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()


def type_print(text, delay=0.004):
    """Быстрая посимвольная печать для ответов ИИ."""
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()


def scan_line(char="─", length=60, color=DIM_GREEN):
    """Горизонтальная разделительная линия."""
    print(f"{color}{char * length}{RESET}")