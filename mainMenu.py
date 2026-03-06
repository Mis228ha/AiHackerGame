"""
mainMenu.py — Главное меню CYBERCORE

Запуск:
    python mainMenu.py

Позволяет выбрать между двумя версиями игры:
  1. CYBERCORE: BREACH PROTOCOL — основная версия (9 файлов)
  2. HACKER HAOS                — хаос-режим (один файл, максимальный шум)
"""

import os
import sys
import time
import subprocess

# ─── ЦВЕТА (встроены чтобы mainMenu не зависел от Colors.py) ─────────────────
GREEN        = "\033[92m"
BRIGHT_GREEN = "\033[1;92m"
DIM_GREEN    = "\033[2;32m"
RED          = "\033[91m"
YELLOW       = "\033[93m"
CYAN         = "\033[96m"
WHITE        = "\033[97m"
MAGENTA      = "\033[95m"
DIM          = "\033[2m"
BOLD         = "\033[1m"
RESET        = "\033[0m"


def slow_print(text, delay=0.016):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()


def scan_line(char="─", length=62, color=DIM_GREEN):
    print(f"{color}{char * length}{RESET}")


# ─── ГЛАВНЫЙ БАННЕР ──────────────────────────────────────────────────────────

MAIN_BANNER = f"""
{BRIGHT_GREEN}
  ██████╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗ ██████╗ ██████╗ ███████╗
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║     ██║   ██║██████╔╝█████╗
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║     ██║   ██║██╔══██╗██╔══╝
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║╚██████╗╚██████╔╝██║  ██║███████╗
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
{RESET}
{DIM_GREEN}                  [ ВЫБОР РЕЖИМА — SELECT YOUR PROTOCOL ]
{RESET}"""


# ─── КАРТОЧКИ ВЕРСИЙ ─────────────────────────────────────────────────────────

CARD_BREACH = f"""
{BRIGHT_GREEN}  ╔══════════════════════════════════════════════════════════════╗
  ║                                                              ║
  ║   1.  ██████╗ ██████╗ ███████╗ █████╗  ██████╗██╗  ██╗     ║
  ║      ██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║     ║
  ║      ██████╔╝██████╔╝█████╗  ███████║██║     ███████║     ║
  ║      ██╔══██╗██╔══██╗██╔══╝  ██╔══██║██║     ██╔══██║     ║
  ║      ██████╔╝██║  ██║███████╗██║  ██║╚██████╗██║  ██║     ║
  ║      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ║
  ║                      PROTOCOL                               ║
  ╠══════════════════════════════════════════════════════════════╣{RESET}
{DIM_GREEN}  ║  Классический хакерский симулятор.                          ║
  ║  Взломай ИИ корпорации NovaCorp — угадай секретный пароль.  ║
  ║                                                              ║
  ║  ▸ 8 ИИ-бэкендов (Claude, GPT, Gemini, Groq и др.)         ║
  ║  ▸ 3 уровня сложности                                       ║
  ║  ▸ Система /hint, /minigame, мини-игры                      ║
  ║  ▸ Достижения, профили, реплеи                              ║
  ║  ▸ Кампания из 5 уровней                                    ║{RESET}
{BRIGHT_GREEN}  ╚══════════════════════════════════════════════════════════════╝{RESET}"""

CARD_HAOS = f"""
{RED}  ╔══════════════════════════════════════════════════════════════╗
  ║                                                              ║
  ║   2.  ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗      ║
  ║      ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗     ║
  ║      ███████║███████║██║     █████╔╝ █████╗  ██████╔╝     ║
  ║      ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗     ║
  ║      ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║     ║
  ║      ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ║
  ║                        HAOS EDITION                         ║
  ╠══════════════════════════════════════════════════════════════╣{RESET}
{DIM_GREEN}  ║  Хаос-режим. Сигнал vs шум.                                 ║
  ║  Среди потока мусорных данных спрятаны настоящие подсказки. ║
  ║                                                              ║
  ║  ▸ Генератор шума: предупреждения, дампы, ложные подсказки  ║
  ║  ▸ Настоящие подсказки помечены [!!] — ищи их              ║
  ║  ▸ /scan для извлечения, /filter для просмотра              ║
  ║  ▸ После победы — выбор судьбы ИИ (5 концовок)             ║
  ║  ▸ Один файл, без зависимостей                              ║{RESET}
{RED}  ╚══════════════════════════════════════════════════════════════╝{RESET}"""


# ─── ЗАПУСК ВЕРСИИ ───────────────────────────────────────────────────────────

def _find_file(names: list) -> str | None:
    """Ищет файл в текущей папке и в подпапках рядом."""
    base = os.path.dirname(os.path.abspath(__file__))
    search_dirs = [
        base,
        os.path.join(base, "AiHackerPassword"),
        os.path.join(base, "hackerHaos"),
        os.path.join(base, "hackerHaos".lower()),
    ]
    for d in search_dirs:
        for name in names:
            path = os.path.join(d, name)
            if os.path.isfile(path):
                return path
    return None


def _run(path: str):
    """
    Запускает Python-скрипт в той же консоли.
    Меняет рабочую директорию на папку скрипта,
    затем передаёт управление через subprocess (работает на Windows/PyCharm).
    После завершения дочернего процесса возвращается в меню.
    """
    import subprocess
    folder = os.path.dirname(os.path.abspath(path))
    try:
        subprocess.run(
            [sys.executable, os.path.basename(path)],
            cwd=folder
        )
    except Exception as e:
        print(f"{RED}  Ошибка запуска: {e}{RESET}")
        input(f"\n{BRIGHT_GREEN}  [ Enter — вернуться в меню ]{RESET}")


def launch_breach():
    """Запускает основную версию BREACH PROTOCOL."""
    path = _find_file(["AiHackerGame.py"])
    if not path:
        print(f"{RED}  Ошибка: AiHackerGame.py не найден.{RESET}")
        print(f"{DIM_GREEN}  Убедись что папка AiHackerPassword/ находится рядом с mainMenu.py{RESET}")
        input(f"\n{BRIGHT_GREEN}  [ Enter — вернуться в меню ]{RESET}")
        return
    _run(path)


def launch_haos():
    """Запускает Hacker Haos Edition."""
    path = _find_file(["HackerHaos.py", "hackerHaos.py", "hacker_haos.py"])
    if not path:
        print(f"{RED}  Ошибка: HackerHaos.py не найден.{RESET}")
        print(f"{DIM_GREEN}  Убедись что папка hackerHaos/ находится рядом с mainMenu.py{RESET}")
        input(f"\n{BRIGHT_GREEN}  [ Enter — вернуться в меню ]{RESET}")
        return
    _run(path)


# ─── ГЛАВНОЕ МЕНЮ ────────────────────────────────────────────────────────────

def main():
    while True:
        os.system("clear" if os.name != "nt" else "cls")
        print(MAIN_BANNER)
        scan_line("═", 62, BRIGHT_GREEN)
        slow_print(f"{DIM_GREEN}  Выбери версию игры и нажми Enter.{RESET}", delay=0.010)
        scan_line("═", 62, BRIGHT_GREEN)

        print(CARD_BREACH)
        print()
        print(CARD_HAOS)
        print()
        scan_line("─", 62, DIM_GREEN)
        print(f"{DIM_GREEN}  0.  Выход{RESET}")
        scan_line("─", 62, DIM_GREEN)
        print()

        try:
            choice = input(f"{BRIGHT_GREEN}  Выбор [1 / 2 / 0]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if choice == "1":
            os.system("clear" if os.name != "nt" else "cls")
            slow_print(f"{BRIGHT_GREEN}  Запуск BREACH PROTOCOL...{RESET}", delay=0.020)
            time.sleep(0.5)
            launch_breach()

        elif choice == "2":
            os.system("clear" if os.name != "nt" else "cls")
            slow_print(f"{RED}  Инициализация HAOS EDITION...{RESET}", delay=0.020)
            time.sleep(0.5)
            launch_haos()

        elif choice == "0":
            break

        else:
            print(f"{RED}  Введи 1, 2 или 0.{RESET}")
            time.sleep(0.8)

    print()
    slow_print(f"{DIM_GREEN}  Соединение закрыто. До следующего взлома.{RESET}", delay=0.015)
    print()


if __name__ == "__main__":
    main()