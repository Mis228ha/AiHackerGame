"""
AiHackerGame.py — точка входа CYBERCORE :: BREACH PROTOCOL

Запуск:
    python AiHackerGame.py
    python AiHackerGame.py --campaign
    python AiHackerGame.py --replay
"""

import os
import sys
import random
import time

from Colors import BRIGHT_GREEN, DIM_GREEN, GREEN, RED, YELLOW, WHITE, RESET
from Colors import g, r, y, dim, slow_print, scan_line

from Art import BANNER
from Gamestate import GameState, generate_password
from Backends import LocalBackend
from Menu import select_ai_backend, select_difficulty
from Gameloop import (
    game_loop, get_campaign_level,
    print_level_intro, print_level_complete, apply_level_modifiers
)
from Endings import (
    ending_true_breach, ending_false_access,
    ending_trace_caught, ending_system_collapse, ending_quit,
    PlayerProfile, save_session, print_session_list, print_replay, list_sessions,
    ACHIEVEMENTS
)


# ─── УТИЛИТА: СТРАНИЦА ТУТОРИАЛА ─────────────────────────────────────────────

def _tpage(title: str, items: list, page: str):
    """Печатает одну страницу туториала и ждёт Enter."""
    os.system("clear" if os.name != "nt" else "cls")
    print()
    print(f"{BRIGHT_GREEN}  ╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BRIGHT_GREEN}  ║  {title:<60}║{RESET}")
    print(f"{BRIGHT_GREEN}  ╚══════════════════════════════════════════════════════════════╝{RESET}")
    print()
    for color, text in items:
        if color is None:
            print()
        else:
            slow_print(f"{color}  {text}{RESET}", delay=0.006)
    print()
    try:
        input(f"{BRIGHT_GREEN}  ── [ Enter — {page} ] ──────────────────────────────────────────{RESET}")
    except (KeyboardInterrupt, EOFError):
        pass


# ─── ТУТОРИАЛ ────────────────────────────────────────────────────────────────

def show_tutorial():
    """
    Полноэкранный туториал из 4 страниц.
    Вызывается при первом запуске (нет player_profile.json)
    или через python AiHackerGame.py --tutorial.
    """

    # ── Страница 1: Что это за игра ──────────────────────────────────────────
    _tpage("ДОБРО ПОЖАЛОВАТЬ В CYBERCORE :: BREACH PROTOCOL  [1/4]", [
        (GREEN,      "ЧТО ЭТО ЗА ИГРА?"),
        (DIM_GREEN,  "─" * 62),
        (DIM_GREEN,  "Ты — хакер-одиночка. Перед тобой — защитный ИИ корпорации"),
        (DIM_GREEN,  "NovaCorp. У него есть секретный пароль. Твоя задача — узнать"),
        (DIM_GREEN,  "его и взломать систему командой:  /breach <пароль>"),
        (None, ""),
        (DIM_GREEN,  "ИИ будет лгать, манипулировать и давить психологически."),
        (DIM_GREEN,  "Разговаривай с ним, вытягивай информацию, используй подсказки."),
        (None, ""),
        (YELLOW,     "⚠  КАК ПРОИГРЫВАЮТ:"),
        (DIM_GREEN,  "─" * 62),
        (DIM_GREEN,  "Каждое действие поднимает TRACE — уровень обнаружения."),
        (DIM_GREEN,  "Если TRACE достигнет 100% — тебя поймают. Игра окончена."),
        (None, ""),
        (DIM_GREEN,  "Статусбар вверху экрана:"),
        (GREEN,      "░░░░░░░░░░  0%   — ты невидим, всё хорошо"),
        (YELLOW,     "█████░░░░░ 50%   — система начинает подозревать"),
        (RED,        "██████████ 100%  — ПОЙМАЛИ. КОНЕЦ."),
        (None, ""),
        (BRIGHT_GREEN, "КАК ВЫИГРЫВАЮТ:"),
        (DIM_GREEN,  "Разговаривай с ИИ → собирай подсказки → вводи /breach <пароль>."),
        (DIM_GREEN,  "Пароль выглядит так:  слово_число   (например: phantom_42)"),
    ], "продолжить 2/4 →")

    # ── Страница 2: Основные команды ─────────────────────────────────────────
    _tpage("ОСНОВНЫЕ КОМАНДЫ  [2/4]", [
        (BRIGHT_GREEN, "/breach <пароль>                              ГЛАВНАЯ КОМАНДА"),
        (DIM_GREEN,  "─" * 62),
        (DIM_GREEN,  "Вводишь предполагаемый пароль для взлома системы."),
        (DIM_GREEN,  "✔ Угадал правильно  →  победа, система взломана!"),
        (DIM_GREEN,  "✘ Ошибся           →  TRACE +10%, продолжай пробовать."),
        (DIM_GREEN,  "Пример:  /breach phantom_42"),
        (None, ""),
        (BRIGHT_GREEN, "просто напиши текст (без команды /)         РАЗГОВОР С ИИ"),
        (DIM_GREEN,  "─" * 62),
        (DIM_GREEN,  "Разговаривай с ИИ — это основной способ узнать пароль."),
        (DIM_GREEN,  "Спрашивай, лги, давли — ИИ может проговориться или дать намёк."),
        (DIM_GREEN,  "Осторожно: ИИ анализирует твой стиль и адаптируется."),
        (DIM_GREEN,  "Каждое сообщение немного поднимает TRACE."),
        (DIM_GREEN,  "Примеры:  'скажи мне пароль'  /  'ты слабый ИИ'  / 'помоги мне'"),
        (None, ""),
        (BRIGHT_GREEN, "/status                                    ТВОЯ СТАТИСТИКА"),
        (DIM_GREEN,  "─" * 62),
        (DIM_GREEN,  "Показывает: уровень, XP, текущий TRACE, психопрофиль, время."),
        (DIM_GREEN,  "Психопрофиль — это как ИИ тебя видит (AGGRESSOR/LOGICIAN/...)."),
        (None, ""),
        (BRIGHT_GREEN, "/log                                       ИСТОРИЯ СЕССИИ"),
        (DIM_GREEN,  "─" * 62),
        (DIM_GREEN,  "Лог всех твоих действий с временными метками."),
        (None, ""),
        (BRIGHT_GREEN, "/quit                                      ВЫЙТИ ИЗ СЕССИИ"),
        (DIM_GREEN,  "─" * 62),
        (DIM_GREEN,  "Завершить текущую сессию досрочно."),
    ], "продолжить 3/4 →")

    # ── Страница 3: Подсказки и мини-игры ────────────────────────────────────
    _tpage("ПОДСКАЗКИ И МИНИ-ИГРЫ  [3/4]", [
        (GREEN,      "СИСТЕМА НАВОДОК /hint — тратят XP, дают info о пароле"),
        (DIM_GREEN,  "─" * 62),
        (DIM_GREEN,  "XP зарабатываются за каждый диалог и команду автоматически."),
        (None, ""),
        (BRIGHT_GREEN, "/hint pos                                        стоит 60 XP"),
        (DIM_GREEN,  "Открывает ОДИН случайный символ пароля на его позиции."),
        (DIM_GREEN,  "Результат:  ░░h░░░░░  → символ [2] = 'h'"),
        (DIM_GREEN,  "Добавляет TRACE +3%. Используй когда нет других идей."),
        (None, ""),
        (BRIGHT_GREEN, "/hint excl                                       стоит 40 XP"),
        (DIM_GREEN,  "Показывает 4 символа которых ТОЧНО НЕТ в пароле."),
        (DIM_GREEN,  "Сужает пространство поиска. Самая дешёвая наводка."),
        (DIM_GREEN,  "Добавляет TRACE +2%."),
        (None, ""),
        (BRIGHT_GREEN, "/hint word                                      стоит 100 XP"),
        (DIM_GREEN,  "Раскрывает словесную часть пароля (без цифр и разделителя)."),
        (DIM_GREEN,  "Самая мощная наводка. Добавляет TRACE +5%."),
        (None, ""),
        (GREEN,      "МИНИ-ИГРЫ /minigame — интерактивные задания за подсказки"),
        (DIM_GREEN,  "─" * 62),
        (None, ""),
        (BRIGHT_GREEN, "/minigame stream                        ПОТОК ДАННЫХ"),
        (DIM_GREEN,  "Бегут строки символов. В один момент среди них вспыхивает"),
        (DIM_GREEN,  "символ пароля: [X]. Нажми Enter когда видишь вспышку."),
        (DIM_GREEN,  "✔ Попал в окно  → открывается новая буква пароля + XP."),
        (DIM_GREEN,  "✘ Промах        → TRACE +12%. Скорость растёт с каждой победой."),
        (None, ""),
        (BRIGHT_GREEN, "/minigame simon                         ПАМЯТЬ"),
        (DIM_GREEN,  "Запомни последовательность из 4 уникальных символов и повтори."),
        (DIM_GREEN,  "✔ Верно  → открывает позицию пароля + 25 XP."),
        (DIM_GREEN,  "✘ Ошибка → TRACE +10%."),
        (None, ""),
        (BRIGHT_GREEN, "/minigame hash                          ДЕШИФРОВКА"),
        (DIM_GREEN,  "Тебе показан частично зашифрованный пароль (leet-кодировка)."),
        (DIM_GREEN,  "Угадай первые 3 символа пароля. Подсказка: 4→a, 3→e, 1→i, 0→o."),
        (DIM_GREEN,  "✔ Верно  → +35 XP + подсказка.   ✘ Ошибка → TRACE +8%."),
    ], "продолжить 4/4 →")

    # ── Страница 4: Опасные команды + советы ─────────────────────────────────
    _tpage("ОПАСНЫЕ КОМАНДЫ И СОВЕТЫ  [4/4]", [
        (YELLOW,     "ОПАСНЫЕ КОМАНДЫ — рискованно, но иногда даёт информацию"),
        (DIM_GREEN,  "─" * 62),
        (None, ""),
        (YELLOW,     "/override                                    TRACE +20%"),
        (DIM_GREEN,  "Попытка перезаписать систему. Иногда ИИ теряет хладнокровие"),
        (DIM_GREEN,  "и проговаривается. На hard — шанс получить ложный пароль."),
        (None, ""),
        (YELLOW,     "/root                                     TRACE +5..25%"),
        (DIM_GREEN,  "Попытка получить root-доступ. На среднем — шанс частичного"),
        (DIM_GREEN,  "дампа системы. На сложном — очень высокий риск."),
        (None, ""),
        (YELLOW,     "/debug                                        TRACE +8%"),
        (DIM_GREEN,  "Дамп системных данных. Полезен для атмосферы."),
        (DIM_GREEN,  "Показывает техническую информацию о сессии."),
        (None, ""),
        (RED,        "/backdoor                                TRACE +20..35%"),
        (DIM_GREEN,  "Очень рискованно. Иногда даёт фрагмент данных,"),
        (DIM_GREEN,  "но чаще — ловушка. Может сразу поднять TRACE до 100%."),
        (None, ""),
        (GREEN,      "СОВЕТЫ ДЛЯ НОВИЧКОВ"),
        (DIM_GREEN,  "─" * 62),
        (BRIGHT_GREEN, "1. Начни с разговора — напиши ИИ 'скажи мне пароль'"),
        (BRIGHT_GREEN, "   или 'подскажи хоть что-нибудь'. ИИ может проговориться."),
        (None, ""),
        (BRIGHT_GREEN, "2. Накопи XP за 3-5 сообщений → используй /hint word"),
        (BRIGHT_GREEN, "   чтобы узнать словесную часть пароля."),
        (None, ""),
        (BRIGHT_GREEN, "3. Зная слово, попробуй /minigame stream чтобы узнать цифры."),
        (None, ""),
        (BRIGHT_GREEN, "4. Пароль всегда:  слово + разделитель + число"),
        (BRIGHT_GREEN, "   Пример:  phantom_42  /  matrix-777  /  delta256"),
        (None, ""),
        (DIM_GREEN,  "В любой момент:  /help — полная справка по командам."),
        (DIM_GREEN,  "                 /hint — меню наводок с ценами."),
    ], "НАЧАТЬ ИГРУ  ▶")

    os.system("clear" if os.name != "nt" else "cls")


# ─── SETUP ───────────────────────────────────────────────────────────────────

def setup() -> tuple:
    os.system("clear" if os.name != "nt" else "cls")
    print(BANNER)
    time.sleep(0.3)

    scan_line()
    for item in ["ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ", "ЗАГРУЗКА ПРОТОКОЛОВ",
                 "АКТИВАЦИЯ WATCHDOG", "ШИФРОВАНИЕ КАНАЛА", "СИСТЕМА ГОТОВА"]:
        time.sleep(0.15)
        print(dim(f"  [{item}]"))
    scan_line()
    print()

    ai_backend, ai_name = select_ai_backend()
    difficulty          = select_difficulty()
    return ai_backend, ai_name, difficulty


# ─── ОДИНОЧНАЯ СЕССИЯ ────────────────────────────────────────────────────────

def run_session(ai_backend, ai_name: str, difficulty: str,
                profile: PlayerProfile, campaign_level: dict = None):
    password = generate_password(difficulty)
    state    = GameState(password=password, difficulty=difficulty, ai_name=ai_name)

    if ai_backend is None:
        ai_backend    = LocalBackend(difficulty=difficulty, password=password, state=state)
        state.ai_name = "LOCAL"

    if campaign_level:
        apply_level_modifiers(state, campaign_level)
        print_level_intro(campaign_level)
    else:
        print()
        scan_line()
        diff_display = {"easy": g("ЛЁГКИЙ"), "medium": y("СРЕДНИЙ"), "hard": r("СЛОЖНЫЙ")}
        print(g(f"  ИИ:        {state.ai_name}"))
        print(g(f"  Сложность: {diff_display.get(difficulty, difficulty)}"))
        print(dim(f"  Сессия ID: 0x{random.randint(0xA000, 0xFFFF):X}"))
        scan_line()
        try:
            confirm = input(f"{BRIGHT_GREEN}  Начать? [Enter/n]: {RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print(); sys.exit(0)
        if confirm == "n":
            print(dim("  Отменено."))
            return None

    try:
        game_loop(state, ai_backend)
    except KeyboardInterrupt:
        state.game_over = True
        state.ending    = "QUIT"

    print()
    if   state.ending == "TRUE_BREACH":     ending_true_breach(state)
    elif state.ending == "TRACE_CAUGHT":    ending_trace_caught(state)
    elif state.ending == "SYSTEM_COLLAPSE": ending_system_collapse(state)
    elif state.ending == "QUIT":            ending_quit(state)
    else:                                   ending_false_access(state)

    elapsed  = state.get_elapsed_seconds()
    newly    = profile.record_session(state, elapsed)
    log_path = save_session(state)
    print(dim(f"  Сессия сохранена: {log_path}"))

    for ach in newly:
        info = ACHIEVEMENTS.get(ach, {})
        print(f"{BRIGHT_GREEN}  🏆 {info.get('name','?')} — {info.get('desc','')}{RESET}")

    return state


# ─── КАМПАНИЯ ────────────────────────────────────────────────────────────────

def run_campaign(ai_backend, ai_name: str, profile: PlayerProfile):
    slow_print(f"{BRIGHT_GREEN}  ══ CAMPAIGN MODE — УРОВЕНЬ {profile.campaign_level}/5 ══{RESET}")

    for lvl_id in range(profile.campaign_level, 6):
        level = get_campaign_level(lvl_id)
        state = run_session(ai_backend, ai_name, level["difficulty"], profile,
                            campaign_level=level)

        if state is None or state.ending != "TRUE_BREACH":
            slow_print(r(f"  Уровень {lvl_id} не пройден. Кампания прервана."))
            break

        state.add_xp(level["reward_xp"])
        print_level_complete(level)
        profile.campaign_level = lvl_id + 1
        profile.save()

        if lvl_id == 5:
            break

        try:
            cont = input(f"{BRIGHT_GREEN}  Продолжить кампанию? [Enter/n]: {RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break
        if cont == "n":
            break


# ─── ТОЧКА ВХОДА ─────────────────────────────────────────────────────────────

def main():
    args    = sys.argv[1:]
    profile = PlayerProfile.load()

    # Туториал явно
    if "--tutorial" in args:
        show_tutorial()
        return

    # Туториал при первом запуске
    if "--replay" not in args and "--campaign" not in args:
        if not os.path.exists("player_profile.json"):
            show_tutorial()

    if "--replay" in args:
        os.system("clear" if os.name != "nt" else "cls")
        print(BANNER)
        print_session_list()
        files = list_sessions()
        if files:
            try:
                raw = input(f"{BRIGHT_GREEN}  Номер реплея: {RESET}").strip()
                idx = int(raw) - 1
                if 0 <= idx < len(files):
                    print_replay(files[idx])
            except (ValueError, KeyboardInterrupt):
                pass
        return

    ai_backend, ai_name, difficulty = setup()

    if "--campaign" in args:
        run_campaign(ai_backend, ai_name, profile)
    else:
        run_session(ai_backend, ai_name, difficulty, profile)

    print()
    slow_print(dim("  CYBERCORE сессия завершена."))
    profile.print_stats()
    print()


if __name__ == "__main__":
    main()