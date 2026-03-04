"""
colors.py — ANSI-цвета, утилиты вывода и разделительные линии.
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


def g(text):
    """Обернуть текст в зелёный цвет терминала."""
    return f"{GREEN}{text}{RESET}"

def bg(text):
    """Обернуть текст в ярко-зелёный цвет."""
    return f"{BRIGHT_GREEN}{text}{RESET}"

def r(text):
    """Обернуть текст в красный цвет (опасность)."""
    return f"{RED}{text}{RESET}"

def y(text):
    """Обернуть текст в жёлтый цвет (предупреждение)."""
    return f"{YELLOW}{text}{RESET}"

def c(text):
    """Обернуть текст в голубой цвет (системные сообщения)."""
    return f"{CYAN}{text}{RESET}"

def dim(text):
    """Приглушённый текст."""
    return f"{DIM_GREEN}{text}{RESET}"


def slow_print(text, delay=0.018):
    """
    Печатает текст посимвольно с задержкой для атмосферного эффекта.

    Параметры:
        text  (str)   — текст для вывода
        delay (float) — задержка между символами в секундах
    """
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()


def type_print(text, delay=0.012):
    """
    Быстрая версия посимвольной печати для ответов ИИ.

    Параметры:
        text  (str)   — текст
        delay (float) — задержка
    """
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()


def scan_line(char="─", length=60, color=DIM_GREEN):
    """
    Выводит горизонтальную разделительную линию.

    Параметры:
        char   (str) — символ линии
        length (int) — длина
        color  (str) — ANSI-цвет
    """
    print(f"{color}{char * length}{RESET}")