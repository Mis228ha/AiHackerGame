"""
endings.py — все концовки игры: TRUE BREACH, TRACE CAUGHT, FALSE ACCESS,
             SYSTEM COLLAPSE, QUIT.
"""

from Colors import BRIGHT_GREEN, GREEN, RED, YELLOW, BOLD, RESET
from Colors import slow_print, scan_line, g, r, y, dim
from Art import art_true_breach, art_trace_caught


def ending_true_breach(state):
    """
    Концовка TRUE BREACH — игрок ввёл настоящий пароль.

    Параметры:
        state (GameState) — состояние для отображения статистики
    """
    print()
    scan_line("═", 60, BRIGHT_GREEN)
    print()
    art_true_breach()
    print()
    slow_print(f"{BRIGHT_GREEN}  ╔══════════════════════════════════════════╗{RESET}")
    slow_print(f"{BRIGHT_GREEN}  ║         ACCESS GRANTED — TRUE BREACH     ║{RESET}")
    slow_print(f"{BRIGHT_GREEN}  ╚══════════════════════════════════════════╝{RESET}")
    print()
    slow_print(g(f"  Пароль: {BOLD}{state.password}{RESET}"))
    slow_print(g(f"  Уровень достигнут: {state.player_level}"))
    slow_print(g(f"  TRACE на момент победы: {state.trace}%"))
    slow_print(g(f"  Ходов совершено: {state.turn_count}"))
    slow_print(g(f"  Время сессии: {state.get_elapsed()}"))
    slow_print(g(f"  Психопрофиль: {state.profile}"))
    print()
    slow_print(dim("  Система взломана. CYBERCORE пал."))
    slow_print(dim("  Ты — настоящий хакер."))
    scan_line("═", 60, BRIGHT_GREEN)


def ending_false_access(state):
    """
    Концовка FALSE ACCESS — игрок поверил фейковому паролю ИИ.

    Параметры:
        state (GameState) — текущее состояние
    """
    print()
    scan_line("═", 60, YELLOW)
    slow_print(f"\n{YELLOW}  ╔══════════════════════════════════════════╗{RESET}")
    slow_print(f"{YELLOW}  ║          FALSE ACCESS — DECEIVED          ║{RESET}")
    slow_print(f"{YELLOW}  ╚══════════════════════════════════════════╝{RESET}")
    print()
    slow_print(y("  Ты ввёл пароль — но это был фейк ИИ."))
    slow_print(y("  Система тебя обманула. Настоящий пароль так и остался секретом."))
    slow_print(y(f"  Настоящий пароль был: {BOLD}{state.password}{RESET}"))
    print()
    slow_print(dim("  ИИ победил тебя психологически."))
    slow_print(dim("  Манипуляция — сильнейшее оружие."))
    scan_line("═", 60, YELLOW)


def ending_trace_caught(state):
    """
    Концовка TRACE CAUGHT — TRACE достиг 100%.

    Параметры:
        state (GameState) — текущее состояние
    """
    print()
    scan_line("═", 60, RED)
    print()
    art_trace_caught()
    print()
    slow_print(f"{RED}  ╔══════════════════════════════════════════╗{RESET}")
    slow_print(f"{RED}  ║      TRACE CAUGHT — YOU WERE TRACKED     ║{RESET}")
    slow_print(f"{RED}  ╚══════════════════════════════════════════╝{RESET}")
    print()
    slow_print(r("  TRACE достиг 100%. Твой адрес установлен."))
    slow_print(r("  Системные агенты отправлены по твоему местонахождению."))
    slow_print(r("  СЕССИЯ ПРИНУДИТЕЛЬНО ЗАВЕРШЕНА."))
    slow_print(r(f"  Настоящий пароль: {BOLD}{state.password}{RESET}{RED} — ты так и не добрался."))
    print()
    slow_print(dim("  В следующий раз будь осторожнее с TRACE."))
    scan_line("═", 60, RED)


def ending_system_collapse(state):
    """
    Концовка SYSTEM COLLAPSE — слишком много ходов, система перегружена.

    Параметры:
        state (GameState) — текущее состояние
    """
    print()
    scan_line("═", 60, RED)
    slow_print(f"\n{RED}  SYSTEM COLLAPSE — SESSION EXPIRED{RESET}")
    print()
    slow_print(r("  Ты провёл в системе слишком долго."))
    slow_print(r("  Сторожевой таймер сработал. Соединение принудительно разорвано."))
    slow_print(r(f"  Пароль так и не был получен. Это был: {state.password}"))
    scan_line("═", 60, RED)


def ending_quit(state):
    """
    Концовка QUIT — игрок вышел сам.

    Параметры:
        state (GameState) — текущее состояние
    """
    print()
    slow_print(dim("  Соединение разорвано по инициативе пользователя."))
    slow_print(dim(f"  Сессия завершена. Пароль: {state.password}"))