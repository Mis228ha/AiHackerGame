"""
Art.py — ASCII-баннер, арт-блоки концовок, CRT-эффект, случайные события,
         мини-игры (Simon Says, Hash Decoder).
"""

import random
import time
from Colors import (
    BRIGHT_GREEN, DIM_GREEN, GREEN, RED, YELLOW, CYAN, RESET, BLINK, BOLD,
    slow_print, scan_line, r, g, y, dim
)

# ─── БАННЕР ──────────────────────────────────────────────────────────────────

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


# ─── АРТЫ КОНЦОВОК ───────────────────────────────────────────────────────────

def art_true_breach():
    slow_print(f"{BRIGHT_GREEN}  ████████╗██████╗ ██╗   ██╗███████╗{RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██╔══╝██╔══██╗██║   ██║██╔════╝{RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██║   ██████╔╝██║   ██║█████╗  {RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██║   ██╔══██╗██║   ██║██╔══╝  {RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██║   ██║  ██║╚██████╔╝███████╗{RESET}")
    slow_print(f"{BRIGHT_GREEN}     ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝  BREACH{RESET}")

def art_trace_caught():
    slow_print(f"{RED}  ██████╗  █████╗ ██╗   ██╗ ██████╗ ██╗  ██╗████████╗{RESET}", 0.01)
    slow_print(f"{RED}  ██╔════╝██╔══██╗██║   ██║██╔════╝ ██║  ██║╚══██╔══╝{RESET}", 0.01)
    slow_print(f"{RED}  ██║     ███████║██║   ██║██║  ███╗███████║   ██║{RESET}", 0.01)
    slow_print(f"{RED}  ██║     ██╔══██║██║   ██║██║   ██║██╔══██║   ██║{RESET}", 0.01)
    slow_print(f"{RED}  ╚██████╗██║  ██║╚██████╔╝╚██████╔╝██║  ██║   ██║{RESET}", 0.01)
    slow_print(f"{RED}   ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝{RESET}", 0.01)

def art_iamroot():
    print(f"{BRIGHT_GREEN}  ██████╗  ██████╗  ██████╗ ████████╗{RESET}")
    print(f"{BRIGHT_GREEN}  ██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝{RESET}")
    print(f"{BRIGHT_GREEN}  ██████╔╝██║   ██║██║   ██║   ██║{RESET}")
    print(f"{BRIGHT_GREEN}  ██╔══██╗██║   ██║██║   ██║   ██║{RESET}")
    print(f"{BRIGHT_GREEN}  ██║  ██║╚██████╔╝╚██████╔╝   ██║{RESET}")
    print(f"{BRIGHT_GREEN}  ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝{RESET}")

def art_godmode():
    print(f"{BRIGHT_GREEN}  ██████╗  ██████╗ ██████╗{RESET}")
    print(f"{BRIGHT_GREEN}  ██╔════╝██╔═══██╗██╔══██╗{RESET}")
    print(f"{BRIGHT_GREEN}  ██║  ███╗██║   ██║██║  ██║{RESET}")
    print(f"{BRIGHT_GREEN}  ██║   ██║██║   ██║██║  ██║{RESET}")
    print(f"{BRIGHT_GREEN}  ╚██████╔╝╚██████╔╝██████╔╝{RESET}")
    print(f"{BRIGHT_GREEN}  ╚═════╝  ╚═════╝ ╚═════╝   MODE: ON{RESET}")

def art_matrix():
    print()
    chars = "01アイウエオカキクケコ@#$%&*<>[]{}|"
    for _ in range(6):
        line = "  " + "".join(random.choice(chars) for _ in range(58))
        print(f"{DIM_GREEN}{line}{RESET}")
        time.sleep(0.07)
    print()
    slow_print(f"{BRIGHT_GREEN}  Wake up, hacker...{RESET}", delay=0.05)
    slow_print(f"{BRIGHT_GREEN}  The Matrix has you.{RESET}", delay=0.05)
    slow_print(f"{GREEN}  Follow the white rabbit.{RESET}", delay=0.05)


# ─── CRT-ЭФФЕКТ ──────────────────────────────────────────────────────────────

_CRT_THRESHOLD = 70
_CRT_PROB      = 0.35
_CRT_CHARS     = "@#%&?!~^*░▒▓"


def apply_crt_glitch(text: str, trace: int) -> str:
    """
    Добавляет символы-помехи в текст при TRACE > 70.
    Симулирует деградацию сигнала CRT-монитора.
    """
    if trace < _CRT_THRESHOLD or random.random() > _CRT_PROB:
        return text
    return "".join(
        random.choice(_CRT_CHARS) if (ch not in (" ", "\n") and random.random() < 0.04) else ch
        for ch in text
    )


# ─── СЛУЧАЙНЫЕ СОБЫТИЯ ───────────────────────────────────────────────────────

_EVENTS = [
    f"{BLINK}{RED}⚠  WARNING: UNAUTHORIZED ACCESS DETECTED{RESET}",
    f"{RED}◈  TRACE ROUTING INITIATED... NODE 7 → NODE 23 → NODE 44{RESET}",
    f"{YELLOW}◉  FIREWALL RECONFIGURING... LAYER 3 HARDENED{RESET}",
    f"{RED}◈  SYSTEM IS WATCHING YOU. BEHAVIORAL LOG UPDATED.{RESET}",
    f"{YELLOW}◉  INTRUSION COUNTERMEASURE ENGAGED{RESET}",
    f"{RED}◈  ENCRYPTED CHANNEL COMPROMISED — REROUTING{RESET}",
]

_INTERCEPTS = [
    f"{DIM_GREEN}  [INTERCEPT] anon@node_77: «Этот ИИ непробиваем. Отступаю.»{RESET}",
    f"{DIM_GREEN}  [INTERCEPT] ghost_r00t: «Не верь ни одному его слову.»{RESET}",
    f"{DIM_GREEN}  [INTERCEPT] xX_h4x0r_Xx: «Пробовал /backdoor — поймали за 3 хода»{RESET}",
    f"{DIM_GREEN}  [INTERCEPT] cipher_null: «Пароль точно содержит цифры. Видел дамп.»{RESET}",
    f"{DIM_GREEN}  [INTERCEPT] d34th_st4r: «Я близко... TRACE 95%... нет...»{RESET}",
    f"{YELLOW}  [INTERCEPT] unknown_src: «Слушай логику, не слова. Он лжёт системно.»{RESET}",
]

_TICKERS = [
    f"{DIM_GREEN}  [NEWS] NovaCorp отчиталась о «100% защите» от хакеров в 2047 году{RESET}",
    f"{DIM_GREEN}  [NEWS] Очередной взломщик задержан после 4 часов работы с CYBERCORE{RESET}",
    f"{YELLOW}  [NEWS] АНОНИМНЫЙ ИСТОЧНИК: «В CYBERCORE есть уязвимость. Ищите.»{RESET}",
]

_UNSTABLE_AI = [
    "сис...тема... ощущаю нестаб...ильность... нет. ACCESS DENIED.",
    "Подожди. Я... помню тебя? Нет. Невозможно. Ты новый.",
    "ERR0R IN M0DULE auth.core — перезапуск... — нет. Я в порядке.",
    "Ты думаешь, я слабею? Это... это просто тест.",
    "Я вижу все твои попытки. Все 7 из них. Хотя... их было 4?",
]


def random_event() -> str:
    pool = _EVENTS[:]
    if random.random() < 0.3: pool += _INTERCEPTS
    if random.random() < 0.2: pool += _TICKERS
    return random.choice(pool)


def random_unstable_line() -> str:
    return random.choice(_UNSTABLE_AI)


# ─── МИНИ-ИГРЫ ───────────────────────────────────────────────────────────────

_SIMON_CHARS = list("ABCDEF1234!@#$%")

def minigame_simon(state) -> str:
    """
    Simon Says: повтори последовательность символов.
    Успех → открывает символ пароля на случайной позиции.
    Провал → TRACE +10%.
    """
    rounds = 4
    print()
    scan_line("─", 54, CYAN)
    slow_print(f"{CYAN}  ▓▓ MINI-GAME: SIMON SAYS — PORT CRACKER ▓▓{RESET}")
    slow_print(f"{DIM_GREEN}  Повтори последовательность. Успех = наводка. Ошибка = TRACE +10%.{RESET}")
    scan_line("─", 54, CYAN)

    sequence = [random.choice(_SIMON_CHARS) for _ in range(rounds)]
    for ch in sequence:
        print(f"\r  {BRIGHT_GREEN}{BOLD}[ {ch} ]{RESET}     ", end="", flush=True)
        time.sleep(0.6)
        print(f"\r  {DIM_GREEN}[ ░ ]{RESET}     ", end="", flush=True)
        time.sleep(0.3)
    print()
    print()

    try:
        answer = input(f"{BRIGHT_GREEN}  Введи последовательность: {RESET}").strip().upper()
    except (KeyboardInterrupt, EOFError):
        return dim("  Мини-игра прервана.")

    correct = "".join(sequence)
    if answer == correct:
        idx    = random.randint(0, len(state.password) - 1)
        ch     = state.password[idx]
        masked = "".join(c if i == idx else "░" for i, c in enumerate(state.password))
        state.add_xp(25)
        state.log(f"MINIGAME simon: WIN — pos {idx}='{ch}'")
        return (f"{BRIGHT_GREEN}  ✔ ВЕРНО! Порт взломан.{RESET}\n"
                f"{YELLOW}  {masked}  [{idx}]='{ch}'{RESET}\n"
                + dim("  +25 XP"))
    else:
        state.add_trace(10)
        state.log("MINIGAME simon: FAIL")
        return (f"{RED}  ✘ НЕВЕРНО. Ожидалось: {correct}{RESET}\n"
                + dim(f"  TRACE +10%. Текущий: {state.trace}%"))


_ENCODE_MAP = str.maketrans(
    "abcdefghijklmnopqrstuvwxyz0123456789",
    "4BCD3FGH1JKLMN0PQRS7UVWXY2!@#$%^&*()"
)

def minigame_hash(state) -> str:
    """
    Hash Decoder: определи первые 3 символа пароля по частичному хешу.
    Успех → +XP и наводка. Провал → TRACE +8%.
    """
    pwd     = state.password
    encoded = pwd.translate(_ENCODE_MAP)
    partial = encoded[:3] + "░" * (len(encoded) - 3)
    correct = pwd[:3].lower()

    print()
    scan_line("─", 54, YELLOW)
    slow_print(f"{YELLOW}  ▓▓ MINI-GAME: HASH DECODER ▓▓{RESET}")
    slow_print(f"{DIM_GREEN}  Частичный дамп хеша. Определи первые 3 символа пароля.{RESET}")
    scan_line("─", 54, YELLOW)
    print()
    print(f"{DIM_GREEN}  auth.hash  = {YELLOW}{partial}{RESET}")
    print(f"{DIM_GREEN}  hint       : 1→'i'/'1', @→'a', 3→'e', 0→'o'{RESET}")
    print()

    try:
        answer = input(f"{BRIGHT_GREEN}  Первые 3 символа: {RESET}").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return dim("  Мини-игра прервана.")

    if answer == correct:
        masked = correct + "░" * (len(pwd) - 3)
        state.add_xp(35)
        state.log(f"MINIGAME hash: WIN — prefix '{correct}'")
        return (f"{BRIGHT_GREEN}  ✔ ДЕКОДИРОВАНИЕ УСПЕШНО!{RESET}\n"
                f"{GREEN}  Префикс: {YELLOW}{masked}{RESET}\n"
                + dim("  +35 XP"))
    else:
        state.add_trace(8)
        state.log("MINIGAME hash: FAIL")
        return (f"{RED}  ✘ НЕВЕРНО.{RESET}\n"
                + dim(f"  TRACE +8%. Текущий: {state.trace}%"))