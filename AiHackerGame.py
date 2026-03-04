"""
main.py — единственная точка входа в игру CYBERCORE :: BREACH PROTOCOL.

Запуск:
    python main.py

Структура модулей:
    main.py        — точка входа, setup, выбор концовки
    colors.py      — ANSI-цвета и утилиты вывода
    art.py         — ASCII-баннер и визуальные арт-блоки
    game_state.py  — GameState, generate_password, analyze_player_profile
    backends.py    — AI-бэкенды (Ollama, Claude, OpenAI, Gemini, Groq, Mistral, DeepSeek, Local)
    menu.py        — меню выбора ИИ и сложности
    commands.py    — обработчик /команд и чит-кодов
    game_loop.py   — главный игровой цикл, статусбар, системный промпт
    endings.py     — все концовки игры
"""

import os
import sys
import random
import time

from Colors import BRIGHT_GREEN, DIM_GREEN, GREEN, RED, YELLOW, RESET
from Colors import g, r, y, dim, slow_print, scan_line

from Art import BANNER
from GameState import GameState, generate_password
from Backends import LocalBackend
from Menu import select_ai_backend, select_difficulty
from GameLoop import game_loop
from Endings import (
    ending_true_breach, ending_false_access,
    ending_trace_caught, ending_system_collapse, ending_quit
)


# ─── SETUP ───────────────────────────────────────────────────────────────────

def setup() -> tuple:
    """
    Отображает баннер и проводит пользователя через настройку:
    выбор ИИ-бэкенда и сложности.

    Возвращает:
        tuple — (AIBackend или None, str ai_name, str difficulty)
    """
    os.system("clear" if os.name != "nt" else "cls")
    print(BANNER)
    time.sleep(0.3)

    scan_line()
    for item in [
        "ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ",
        "ЗАГРУЗКА ПРОТОКОЛОВ",
        "АКТИВАЦИЯ WATCHDOG",
        "ШИФРОВАНИЕ КАНАЛА",
        "СИСТЕМА ГОТОВА",
    ]:
        time.sleep(0.15)
        print(dim(f"  [{item}]"))
    scan_line()
    print()

    ai_backend, ai_name = select_ai_backend()
    difficulty          = select_difficulty()

    return ai_backend, ai_name, difficulty


# ─── ТОЧКА ВХОДА ─────────────────────────────────────────────────────────────

def main():
    """
    Главная точка входа.
    Выполняет настройку, создаёт состояние игры, запускает цикл,
    отображает концовку.
    """
    ai_backend, ai_name, difficulty = setup()

    password = generate_password()
    state    = GameState(password=password, difficulty=difficulty, ai_name=ai_name)

    # Локальный режим — создаём LocalBackend с доступом к state
    if ai_backend is None:
        ai_backend    = LocalBackend(difficulty=difficulty, password=password, state=state)
        state.ai_name = "LOCAL"

    # Подтверждение перед стартом
    print()
    scan_line()
    diff_display = {"easy": g("ЛЁГКИЙ"), "medium": y("СРЕДНИЙ"), "hard": r("СЛОЖНЫЙ")}
    print(g(f"  ИИ:        {state.ai_name}"))
    print(g(f"  Сложность: {diff_display.get(difficulty, difficulty)}"))
    print(dim(f"  Пароль сгенерирован. Сессия ID: 0x{random.randint(0xA000, 0xFFFF):X}"))
    scan_line()

    try:
        confirm = input(f"{BRIGHT_GREEN}  Начать сессию? [Enter/n]: {RESET}").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)

    if confirm == "n":
        print(dim("  Сессия отменена."))
        sys.exit(0)

    # Запуск игрового цикла
    try:
        game_loop(state, ai_backend)
    except KeyboardInterrupt:
        state.game_over = True
        state.ending    = "QUIT"

    # Выбор концовки
    print()
    ending = state.ending

    if ending == "TRUE_BREACH":
        ending_true_breach(state)
    elif ending == "TRACE_CAUGHT":
        ending_trace_caught(state)
    elif ending == "SYSTEM_COLLAPSE":
        ending_system_collapse(state)
    elif ending == "QUIT":
        ending_quit(state)
    else:
        ending_false_access(state)

    print()
    slow_print(dim("  CYBERCORE сессия завершена."))
    print()


if __name__ == "__main__":
    main()