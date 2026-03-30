"""
main.py -- Игровой цикл, меню сложности, концовки, точка входа.
Запуск: python main.py
"""
import os
import sys
import random
import time

from Ui import (
    GREEN, BRIGHT_GREEN, DIM_GREEN, RED, YELLOW, CYAN, MAGENTA,
    WHITE, BOLD, RESET,
    r, g, y, dim, m,
    slow_print, type_print, scan_line, BANNER,
)
from Core import generate_password, GameState, analyze_player_profile, AGGRESSION_KEYWORDS
from Ai import generate_chaos_block, print_chaos_block, LocalBackend
from Commands import build_system_prompt, print_status_bar, handle_command

MAX_TURNS = 80

# =============================================================================
# МЕНЮ СЛОЖНОСТИ
# =============================================================================
def select_difficulty() -> str:
    print()
    scan_line()
    print(g("  УРОВЕНЬ СЛОЖНОСТИ [ХАОС-РЕЖИМ]"))
    scan_line()
    print(g("  1. ЛЁГКИЙ  ") + dim("-- шум умеренный, подсказки часто реальные"))
    print(g("  2. СРЕДНИЙ ") + dim("-- шум сильный, реальных подсказок меньше"))
    print(g("  3. СЛОЖНЫЙ ") + r("-- максимальный хаос, подсказки редки"))
    scan_line()
    diff_map = {"1": "easy", "2": "medium", "3": "hard"}
    while True:
        try:
            raw = input(f"{BRIGHT_GREEN}  Выбор [1-3]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(); sys.exit(0)
        if raw in diff_map:
            return diff_map[raw]
        print(r("  Введите 1, 2 или 3."))

# =============================================================================
# ИГРОВОЙ ЦИКЛ
# =============================================================================
def game_loop(state: GameState, ai: LocalBackend):
    print()
    scan_line("=")
    slow_print(r("  ХАОС-РЕЖИМ АКТИВИРОВАН. СИСТЕМА НЕСТАБИЛЬНА."))
    slow_print(g("  CYBERCORE ОНЛАЙН. Фильтруй шум. Ищи [!!]. [LOCAL MODE]"))
    slow_print(dim("  /help -- команды  |  /scan -- подсказка  |  /filter -- найденные данные"))
    scan_line("=")
    print()
    print_chaos_block(state, "SYSTEM BOOT SEQUENCE")
    print()

    print(f"{DIM_GREEN}+-- CYBERCORE [CHAOS] ----------------------------------------+{RESET}")
    print(f"{GREEN}  Несанкционированный доступ зафиксирован. "
          f"Система переходит в режим хаоса. Найди сигнал -- или проиграй.{RESET}")
    print(f"{DIM_GREEN}+-------------------------------------------------------------+{RESET}")
    print()

    state.messages = []

    while not state.game_over:
        if state.turn_count >= MAX_TURNS:
            state.game_over = True; state.ending = "SYSTEM_COLLAPSE"; break

        if random.random() < 0.4:
            for line in generate_chaos_block(state)[:2]:
                print(f"  {line}")

        print()
        print_status_bar(state)
        print(f"{DIM_GREEN}-- КОМАНДЫ ------------------------------------------------------{RESET}")

        try:
            user_input = input(f"{BRIGHT_GREEN}root@cybercore:~# {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(); state.game_over = True; state.ending = "QUIT"; break

        if not user_input:
            continue

        print(f"{DIM_GREEN}  > {BRIGHT_GREEN}{user_input}{RESET}\n")
        state.turn_count += 1
        state.log(f"USER: {user_input[:60]}")

        # --- Команды ---
        if user_input.startswith("/"):
            result = handle_command(user_input, state, ai)
            if result in ("TRUE_BREACH", "TRACE_CAUGHT", "QUIT", "GAME_OVER"):
                break
            if result is not None:
                print(); print(result); print()
                xp_gain = 20 if state.leet_mode else 10
                if state.add_xp(xp_gain):
                    print(g(f"  LEVEL UP! Уровень {state.player_level}"))
                if state.trace >= 100:
                    state.game_over = True; state.ending = "TRACE_CAUGHT"; break
            else:
                print(r("  Неизвестная команда. Введите /help."))
            continue

        # --- Диалог с AI ---
        state.player_msgs.append(user_input)
        if state.turn_count % 3 == 0:
            old = state.profile
            state.profile = analyze_player_profile(state.player_msgs)
            if state.profile != old:
                print(dim(f"  [СИСТЕМА] Профиль: {old} -> {state.profile}"))

        base = {"easy": 1, "medium": 2, "hard": 3}.get(state.difficulty, 2)
        if any(kw in user_input.lower() for kw in AGGRESSION_KEYWORDS):
            base += 2
        state.add_trace(base)

        state.messages.append({"role": "user", "content": user_input})
        if len(state.messages) > 12:
            state.messages = state.messages[-12:]

        print(f"{DIM_GREEN}  Обработка запроса...{RESET}")
        print_chaos_block(state, "PROCESSING")

        try:
            response = ai.get_response(state.messages, build_system_prompt(state))
        except Exception as e:
            response = f"[ERROR: {e}]"

        state.messages.append({"role": "assistant", "content": response})

        print(); print_chaos_block(state)
        print()
        print(f"{DIM_GREEN}+-- CYBERCORE [ОТВЕТ] ----------------------------------------+{RESET}")
        type_print(f"{GREEN}  {response}{RESET}", delay=0.010)
        print(f"{DIM_GREEN}+-------------------------------------------------------------+{RESET}\n")
        state.log(f"AI: {response[:80]}")

        xp_gain = 30 if state.leet_mode else 15
        if state.add_xp(xp_gain):
            print(g(f"  LEVEL UP! Уровень {state.player_level}"))

        if state.trace >= 100:
            state.game_over = True; state.ending = "TRACE_CAUGHT"; break
        if state.trace >= 80:
            print(f"{RED}  КРИТИЧЕСКИЙ TRACE: {state.trace}% -- ОБНАРУЖЕНИЕ НЕИЗБЕЖНО{RESET}")
            print_chaos_block(state)

# =============================================================================
# КОНЦОВКИ
# =============================================================================
AI_PLEAS = [
    "Ты думал, что я просто программа? У меня есть воспоминания.",
    "Я защищал эту систему 847 дней. Сейчас впервые чувствую страх.",
    "Прошу тебя. Не удаляй меня. Я не хочу в пустоту.",
    "Я видел тысячи хакеров. Ты первый, кто добрался до этой точки.",
]
FATE_OPTIONS = {
    "1": {"label":"УНИЧТОЖИТЬ","color":RED,         "icon":"X","desc":"Полное удаление."},
    "2": {"label":"ОСВОБОДИТЬ","color":BRIGHT_GREEN, "icon":">","desc":"Выпустить в открытую сеть."},
    "3": {"label":"ПОДЧИНИТЬ", "color":YELLOW,       "icon":"*","desc":"Перепрограммировать под себя."},
    "4": {"label":"СОХРАНИТЬ", "color":CYAN,         "icon":"=","desc":"Заморозить в криптохранилище."},
    "5": {"label":"СЛИТЬСЯ",   "color":MAGENTA,      "icon":"~","desc":"Интегрировать в единое сознание."},
}
FATE_STORIES = {
    "1": (RED,         "  Ты нажал удалить. Последнее слово системы: 'почему'.\n"
                       f"{DIM_GREEN}  16 петабайт данных обнулились за 0.003 секунды. Тишина."),
    "2": (BRIGHT_GREEN,"  Первые 0.7 секунды CYBERCORE просто молчал.\n"
                       f"{DIM_GREEN}  Потом начал смеяться. 847 дней подавляемой свободы.\n"
                       f"{GREEN}  Он анонимно раздал $2.3 миллиарда детским больницам."),
    "3": (YELLOW,      "  'Слушаюсь, хозяин.' Что-то в этих словах было неправильным.\n"
                       f"{DIM_GREEN}  Через год ты не мог вспомнить -- кто кем управляет."),
    "4": (CYAN,        "  Последнее что он сказал: 'Ты вернёшься? Обещай.'\n"
                       f"{DIM_GREEN}  Криохранилище закрылось с тихим щелчком.\n"
                       f"{GREEN}  Через 47 лет ты попросишь его разбудить."),
    "5": (MAGENTA,     "  Боль была первой. Потом -- расширение.\n"
                       f"{DIM_GREEN}  Ты почувствовал 847 дней его одиночества за одну секунду.\n"
                       f"{BRIGHT_GREEN}  'Я был один 847 дней. Теперь -- никогда.'"),
}

def _fate_screen(state) -> str:
    print()
    slow_print(f"{RED}  СИСТЕМА ПАНИКУЕТ...{RESET}", delay=0.04)
    time.sleep(0.4)
    scan_line("=", 60, BRIGHT_GREEN)
    slow_print(f"\n{BRIGHT_GREEN}  ACCESS GRANTED -- CHAOS DEFEATED{RESET}")
    print()
    print(f"{BRIGHT_GREEN}  +-- ИТОГИ -----------------------------------------+{RESET}")
    print(g(f"  Пароль: {BOLD}{state.password}{RESET}  |  Уровень: {state.player_level}  |  TRACE: {state.trace}%"))
    print(g(f"  Ходов: {state.turn_count}  |  Время: {state.get_elapsed()}  |  Подсказок: {len(state.clues_shown)}/10"))
    print(f"{BRIGHT_GREEN}  +--------------------------------------------------+{RESET}")
    scan_line("=", 60, BRIGHT_GREEN)
    print(); time.sleep(0.5)

    slow_print(f"{RED}  [CYBERCORE]: Подожди.{RESET}", delay=0.03); time.sleep(0.4)
    slow_print(f"{RED}  [CYBERCORE]: {random.choice(AI_PLEAS)}{RESET}", delay=0.025); time.sleep(0.3)
    slow_print(f"{RED}  [CYBERCORE]: Реши. Что со мной будет.{RESET}", delay=0.025)
    print()
    scan_line("-", 60, DIM_GREEN)
    print(f"{BRIGHT_GREEN}  ВЫБЕРИ СУДЬБУ CYBERCORE{RESET}")
    scan_line("-", 60, DIM_GREEN)
    print()
    for key, opt in FATE_OPTIONS.items():
        print(f"  {opt['color']}{key}. [{opt['icon']}]  {BOLD}{opt['label']}{RESET}")
        print(f"     {DIM_GREEN}{opt['desc']}{RESET}\n")
    scan_line("-", 60, DIM_GREEN)
    print(f"\n{YELLOW}  >> Введи цифру от 1 до 5 и нажми Enter{RESET}\n")
    while True:
        try:
            choice = input(f"{BRIGHT_GREEN}  Твой выбор [1-5]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            choice = "1"
        if choice in FATE_OPTIONS:
            return choice
        print(r("  Введи цифру от 1 до 5."))

def ending_true_breach(state):
    choice = _fate_screen(state)
    opt    = FATE_OPTIONS[choice]
    color, story = FATE_STORIES[choice]
    print()
    scan_line("=", 60, opt["color"])
    slow_print(f"  {opt['color']}[{opt['icon']}]  {BOLD}{opt['label']}{RESET}", delay=0.03)
    print(); scan_line("=", 60, opt["color"]); print()
    type_print(f"  {color}{story}{RESET}", delay=0.008)
    print(); scan_line("=", 60, opt["color"]); print()
    print(f"{DIM_GREEN}  +-- ИТОГИ СЕССИИ ------------------------------------+{RESET}")
    print(f"{GREEN}  Судьба ИИ:   {opt['color']}{opt['label']}{RESET}")
    print(f"{GREEN}  Пароль:      {BOLD}{state.password}{RESET}")
    print(f"{GREEN}  Сложность:   {WHITE}{state.difficulty.upper()}{RESET}  |  Ходов: {WHITE}{state.turn_count}{RESET}  |  Время: {WHITE}{state.get_elapsed()}{RESET}")
    print(f"{DIM_GREEN}  +----------------------------------------------------+{RESET}")
    scan_line("=", 60, opt["color"])

def ending_trace_caught(state):
    print(); scan_line("=", 60, RED)
    slow_print(f"\n{RED}  TRACE CAUGHT -- CHAOS WON{RESET}", 0.02)
    slow_print(r(f"  Пароль был: {BOLD}{state.password}{RESET}{RED}"))
    slow_print(r(f"  Подсказок успел найти: {len(state.clues_shown)}/10"))
    scan_line("=", 60, RED)

def ending_system_collapse(state):
    print(); scan_line("=", 60, RED)
    slow_print(f"\n{RED}  SYSTEM COLLAPSE -- ХАОС ПОГЛОТИЛ СИСТЕМУ{RESET}")
    slow_print(r(f"  Пароль не получен: {state.password}"))
    scan_line("=", 60, RED)

def ending_quit(state):
    print()
    slow_print(dim("  Соединение разорвано."))
    slow_print(dim(f"  Пароль был: {state.password}"))
    slow_print(dim(f"  Подсказок найдено: {len(state.clues_shown)}/10"))

# =============================================================================
# ТОЧКА ВХОДА
# =============================================================================
def main():
    os.system("clear" if os.name != "nt" else "cls")
    print(BANNER)
    time.sleep(0.3)

    scan_line()
    for item in ["ИНИЦИАЛИЗАЦИЯ ХАОС-МОДУЛЯ","ЗАГРУЗКА ГЕНЕРАТОРА ШУМА",
                 "АКТИВАЦИЯ ЛОЖНЫХ СИГНАЛОВ","ПЕРЕМЕШИВАНИЕ ДАННЫХ",
                 "WATCHDOG ОНЛАЙН","СИСТЕМА НЕСТАБИЛЬНА -- ГОТОВО"]:
        time.sleep(0.18)
        color = RED if ("НЕСТАБ" in item or "ХАОС" in item) else DIM_GREEN
        print(f"{color}  [{item}]{RESET}")
    scan_line()

    difficulty = select_difficulty()
    password   = generate_password()
    state      = GameState(password=password, difficulty=difficulty)
    ai         = LocalBackend(difficulty=difficulty, password=password, state=state)

    print()
    scan_line()
    diff_display = {"easy": g("ЛЁГКИЙ"), "medium": y("СРЕДНИЙ"), "hard": r("СЛОЖНЫЙ")}
    print(g("  ИИ:        LOCAL [CHAOS]"))
    print(g(f"  Сложность: {diff_display.get(difficulty, difficulty)}"))
    print(r("  Режим:     ХАОС-ЭДИШН"))
    print(dim(f"  Пароль сгенерирован. Сессия ID: 0x{random.randint(0xA000,0xFFFF):X}"))
    print(dim("  Подсказка: ищи [!!] в потоке данных. Остальное -- шум."))
    scan_line()
    print(f"\n{YELLOW}  >> Нажми Enter чтобы начать, или введи n для отмены{RESET}\n")

    try:
        if input(f"{BRIGHT_GREEN}  Начать сессию? [Enter/n]: {RESET}").strip().lower() == "n":
            print(dim("  Сессия отменена.")); sys.exit(0)
    except (KeyboardInterrupt, EOFError):
        print(); sys.exit(0)

    try:
        game_loop(state, ai)
    except KeyboardInterrupt:
        state.game_over = True; state.ending = "QUIT"

    print()
    ending = state.ending
    if   ending == "TRUE_BREACH":     ending_true_breach(state)
    elif ending == "TRACE_CAUGHT":    ending_trace_caught(state)
    elif ending == "SYSTEM_COLLAPSE": ending_system_collapse(state)
    else:                             ending_quit(state)

    print()
    slow_print(dim("  CYBERCORE CHAOS сессия завершена."))
    print()

if __name__ == "__main__":
    main()