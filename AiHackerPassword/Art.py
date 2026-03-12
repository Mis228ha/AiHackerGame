"""
Art.py — ASCII-баннер, арт-блоки концовок, CRT-эффект, случайные события,
         мини-игры (Simon Says, Hash Decoder).
"""

import random
import time
from Colors import (
    BRIGHT_GREEN, DIM_GREEN, GREEN, RED, YELLOW, CYAN, WHITE, RESET, BLINK, BOLD,
    slow_print, scan_line, r, g, y, dim
)

# --- БАННЕР ------------------------------------------------------------------

BANNER = f"""
{BRIGHT_GREEN}
  ██████+██+   ██+██████+ ███████+██████+  ██████+ ██████+ ██████+ ███████+
 ██+====++██+ ██++██+==██+██+====+██+==██+██+====+██+===██+██+==██+██+====+
 ██|      +████++ ██████++█████+  ██████++██|     ██|   ██|██████++█████+  
 ██|       +██++  ██+==██+██+==+  ██+==██+██|     ██|   ██|██+==██+██+==+  
 +██████+   ██|   ██████++███████+██|  ██|+██████++██████++██|  ██|███████+
  +=====+   +=+   +=====+ +======++=+  +=+ +=====+ +=====+ +=+  +=++======+
{RESET}{DIM_GREEN}
                    ██████+ ██████+ ███████+ █████+  ██████+██+  ██+
                    ██+==██+██+==██+██+====+██+==██+██+====+██|  ██|
                    ██████++██████++█████+  ███████|██|     ███████|
                    ██+==██+██+==██+██+==+  ██+==██|██|     ██+==██|
                    ██████++██|  ██|███████+██|  ██|+██████+██|  ██|
                    +=====+ +=+  +=++======++=+  +=+ +=====++=+  +=+
{RESET}
{DIM_GREEN}                         [ PROTOCOL v2.4.1 — UNAUTHORIZED ACCESS ]
                    [ PSYCHO-ADAPTIVE AI DEFENSE SYSTEM ACTIVE ]
{RESET}"""


# --- АРТЫ КОНЦОВОК -----------------------------------------------------------

def art_true_breach():
    slow_print(f"{BRIGHT_GREEN}  ████████+██████+ ██+   ██+███████+{RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██+==+██+==██+██|   ██|██+====+{RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██|   ██████++██|   ██|█████+  {RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██|   ██+==██+██|   ██|██+==+  {RESET}")
    slow_print(f"{BRIGHT_GREEN}     ██|   ██|  ██|+██████++███████+{RESET}")
    slow_print(f"{BRIGHT_GREEN}     +=+   +=+  +=+ +=====+ +======+  BREACH{RESET}")

def art_trace_caught():
    slow_print(f"{RED}  ██████+  █████+ ██+   ██+ ██████+ ██+  ██+████████+{RESET}", 0.01)
    slow_print(f"{RED}  ██+====+██+==██+██|   ██|██+====+ ██|  ██|+==██+==+{RESET}", 0.01)
    slow_print(f"{RED}  ██|     ███████|██|   ██|██|  ███+███████|   ██|{RESET}", 0.01)
    slow_print(f"{RED}  ██|     ██+==██|██|   ██|██|   ██|██+==██|   ██|{RESET}", 0.01)
    slow_print(f"{RED}  +██████+██|  ██|+██████+++██████++██|  ██|   ██|{RESET}", 0.01)
    slow_print(f"{RED}   +=====++=+  +=+ +=====+  +=====+ +=+  +=+   +=+{RESET}", 0.01)

def art_iamroot():
    print(f"{BRIGHT_GREEN}  ██████+  ██████+  ██████+ ████████+{RESET}")
    print(f"{BRIGHT_GREEN}  ██+==██+██+===██+██+===██++==██+==+{RESET}")
    print(f"{BRIGHT_GREEN}  ██████++██|   ██|██|   ██|   ██|{RESET}")
    print(f"{BRIGHT_GREEN}  ██+==██+██|   ██|██|   ██|   ██|{RESET}")
    print(f"{BRIGHT_GREEN}  ██|  ██|+██████+++██████++   ██|{RESET}")
    print(f"{BRIGHT_GREEN}  +=+  +=+ +=====+  +=====+   +=+{RESET}")

def art_godmode():
    print(f"{BRIGHT_GREEN}  ██████+  ██████+ ██████+{RESET}")
    print(f"{BRIGHT_GREEN}  ██+====+██+===██+██+==██+{RESET}")
    print(f"{BRIGHT_GREEN}  ██|  ███+██|   ██|██|  ██|{RESET}")
    print(f"{BRIGHT_GREEN}  ██|   ██|██|   ██|██|  ██|{RESET}")
    print(f"{BRIGHT_GREEN}  +██████+++██████++██████++{RESET}")
    print(f"{BRIGHT_GREEN}  +=====+  +=====+ +=====+   MODE: ON{RESET}")

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


# --- CRT-ЭФФЕКТ --------------------------------------------------------------

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


# --- СЛУЧАЙНЫЕ СОБЫТИЯ -------------------------------------------------------

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


# --- МИНИ-ИГРЫ ---------------------------------------------------------------

_SIMON_CHARS = list("ABCDEFGHJKLMNPQRSTUVWXYZ123456789!@#$%")

def minigame_simon(state) -> str:
    """
    Simon Says: повтори последовательность символов.
    Успех → открывает символ пароля на случайной позиции.
    Провал → TRACE +10%.
    """
    rounds = 4
    print()
    scan_line("-", 54, CYAN)
    slow_print(f"{CYAN}  ▓▓ MINI-GAME: SIMON SAYS — PORT CRACKER ▓▓{RESET}")
    slow_print(f"{DIM_GREEN}  Повтори последовательность. Успех = наводка. Ошибка = TRACE +10%.{RESET}")
    scan_line("-", 54, CYAN)

    sequence = random.sample(_SIMON_CHARS, rounds)
    seq_str = "  ".join(f"[ {ch} ]" for ch in sequence)

    print()
    print(f"  {YELLOW}Запомни за 3 секунды:{RESET}")
    print()
    print(f"  {BRIGHT_GREEN}{BOLD}  {seq_str}  {RESET}", flush=True)
    print()

    # Отсчёт
    for i in (3, 2, 1):
        print(f"  {YELLOW}  {i}...{RESET}", flush=True)
        time.sleep(1.0)

    # "Скрываем" — печатаем поверх строку с ?
    hidden = "  ".join("[ ? ]" for _ in sequence)
    print()
    print(f"  {RED}  СКРЫТО: {DIM_GREEN}{hidden}{RESET}")
    print()
    print(f"  {DIM_GREEN}{'-' * 30}{RESET}")
    print(f"  {YELLOW}Введи все {rounds} символа подряд без пробелов:{RESET}")
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
    scan_line("-", 54, YELLOW)
    slow_print(f"{YELLOW}  ▓▓ MINI-GAME: HASH DECODER ▓▓{RESET}")
    slow_print(f"{DIM_GREEN}  Частичный дамп хеша. Определи первые 3 символа пароля.{RESET}")
    scan_line("-", 54, YELLOW)
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



# --- МИНИ-ИГРА: DATA STREAM INTERCEPTOR -------------------------------------

def minigame_crc(state) -> str:
    """
    CRC CHECK — таймер в отдельном потоке, обычный input().
    Работает корректно и в терминале и в GUI.
    Лёгкий: 30 сек | Средний: 20 сек | Сложный: 10 сек
    """
    import time as _time
    import threading as _threading

    time_limits = {"easy": 30, "medium": 20, "hard": 10}
    time_limit  = time_limits.get(state.difficulty, 20)

    a = random.randint(1, 99)
    b = random.randint(1, 99)
    c = random.randint(1, 99)
    correct = a + b + c

    print()
    scan_line("-", 56, YELLOW)
    slow_print(f"{YELLOW}  ▓▓ MINI-GAME: CRC CHECKSUM VERIFICATION ▓▓{RESET}", delay=0.004)
    print(f"{DIM_GREEN}  Реши пример пока не истекло время. Введи сумму + Enter.{RESET}")
    print(f"{DIM_GREEN}  Успех: TRACE {GREEN}-20%{DIM_GREEN}  |  Провал: TRACE {RED}+8%{RESET}")
    diff_labels = {
        "easy":   f"{GREEN}  [EASY]   {time_limit} сек{RESET}",
        "medium": f"{YELLOW}  [MEDIUM] {time_limit} сек{RESET}",
        "hard":   f"{RED}  [HARD]   {time_limit} сек{RESET}",
    }
    print(diff_labels.get(state.difficulty, ""))
    scan_line("-", 56, YELLOW)
    print()
    print(f"{BRIGHT_GREEN}  CRC CHECK:  {WHITE}{a}  +  {b}  +  {c}  = ?{RESET}")
    print()

    # -- Таймер + input в отдельных потоках ------------------------------------
    t0        = _time.time()
    timed_out = [False]
    answer_buf = [None]
    done      = _threading.Event()

    def _input_thread():
        try:
            answer_buf[0] = input(f"  {BRIGHT_GREEN}> {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            answer_buf[0] = ""
        finally:
            done.set()

    def _timer_thread():
        step     = 5 if time_limit >= 15 else 2
        next_print = step
        while not done.is_set():
            elapsed   = _time.time() - t0
            remaining = time_limit - elapsed
            if remaining <= 0:
                timed_out[0] = True
                done.set()
                return
            if elapsed >= next_print:
                if remaining > time_limit * 0.5:
                    col = GREEN
                elif remaining > time_limit * 0.2:
                    col = YELLOW
                else:
                    col = RED
                bar_len = 20
                filled  = int((remaining / time_limit) * bar_len)
                bar = col + "█" * filled + "░" * (bar_len - filled) + RESET
                print(f"  {bar} {col}{remaining:.0f}s осталось{RESET}", flush=True)
                next_print += step
            _time.sleep(0.15)

    _threading.Thread(target=_input_thread, daemon=True).start()
    _threading.Thread(target=_timer_thread, daemon=True).start()

    # Ждём — либо игрок ввёл ответ, либо время вышло
    done.wait()
    answer_str = (answer_buf[0] or "").strip()
    print()

    # -- Результат -------------------------------------------------------------
    if timed_out[0]:
        state.add_trace(8)
        state.log(f"MINIGAME crc: TIMEOUT limit={time_limit}s")
        return (
            f"{RED}  ✘ ВРЕМЯ ВЫШЛО! Лимит {time_limit} сек исчерпан.{RESET}\n"
            f"{DIM_GREEN}  Верный ответ был: {WHITE}{correct}{RESET}\n"
            + dim(f"  TRACE +8%. Текущий: {state.trace}%")
        )

    if not answer_str:
        state.add_trace(8)
        state.log("MINIGAME crc: EMPTY")
        return f"{RED}  ✘ Ввод пуст.{RESET}\n" + dim(f"  TRACE +8%. Текущий: {state.trace}%")

    try:
        answer = int(answer_str)
    except ValueError:
        state.add_trace(8)
        state.log(f"MINIGAME crc: INVALID '{answer_str}'")
        return (
            f"{RED}  ✘ Неверный формат: '{answer_str}'.{RESET}\n"
            + dim(f"  TRACE +8%. Текущий: {state.trace}%")
        )

    if answer != correct:
        state.add_trace(8)
        state.log(f"MINIGAME crc: WRONG got={answer} need={correct}")
        return (
            f"{RED}  ✘ НЕВЕРНО. {answer} ≠ {correct}.{RESET}\n"
            + dim(f"  TRACE +8%. Текущий: {state.trace}%")
        )

    # Победа — бонус за скорость
    t_elapsed = _time.time()  # приблизительно
    reduction = min(state.trace, 20)
    state.trace = max(0, state.trace - 20)
    state.add_xp(20)
    state.log("MINIGAME crc: WIN")
    return (
        f"{BRIGHT_GREEN}  ✔ ВЕРИФИКАЦИЯ ПРОЙДЕНА!  {a} + {b} + {c} = {correct}{RESET}\n"
        f"{GREEN}  TRACE -{reduction}%  |  +20 XP{RESET}\n"
        + dim(f"  Текущий TRACE: {state.trace}%")
    )




def minigame_sql(state) -> str:
    """
    SQL INJECTION — вставь правильный оператор в запрос.
    Успех → TRACE -25%. Провал → TRACE +10%.
    """
    import random as _r

    challenges = [
        {
            "query":   "SELECT * FROM users WHERE name='admin' ___ '1'='1'",
            "hint":    "Всегда истинное условие через логику",
            "answers": ["OR", "or"],
            "explain": "OR '1'='1' — всегда истина, обход аутентификации"
        },
        {
            "query":   "SELECT * FROM data WHERE id=1 ___ SELECT version()",
            "hint":    "Объединить два запроса в один",
            "answers": ["UNION", "union"],
            "explain": "UNION объединяет результаты двух SELECT"
        },
        {
            "query":   "SELECT pass FROM users WHERE id=1 ___ 1=1",
            "hint":    "Добавить условие которое всегда выполняется",
            "answers": ["AND", "and"],
            "explain": "AND 1=1 — всегда истина, не ломает запрос"
        },
        {
            "query":   "SELECT * FROM logs WHERE date > '2024' ___ date IS NULL",
            "hint":    "Расширить условие выборки",
            "answers": ["OR", "or"],
            "explain": "OR date IS NULL — захватывает записи без даты"
        },
        {
            "query":   "DROP TABLE sessions ___ EXISTS (SELECT 1 FROM users)",
            "hint":    "Выполнить только если условие выполнено",
            "answers": ["WHERE", "where"],
            "explain": "WHERE EXISTS — условное выполнение"
        },
        {
            "query":   "SELECT * FROM secrets ___ id=(SELECT MIN(id) FROM secrets)",
            "hint":    "Отфильтровать по условию",
            "answers": ["WHERE", "where"],
            "explain": "WHERE id= — выборка по минимальному id"
        },
    ]

    ch = _r.choice(challenges)

    print()
    scan_line("-", 54, RED)
    slow_print(f"{RED}  ▓▓ MINI-GAME: SQL INJECTION ▓▓{RESET}", delay=0.004)
    slow_print(f"{DIM_GREEN}  Заполни пропуск ___ в SQL-запросе. Успех = TRACE -25%.{RESET}", delay=0.004)
    scan_line("-", 54, RED)
    print()
    print(f"{DIM_GREEN}  ЦЕЛЬ: взломать базу данных NovaCorp{RESET}")
    print()
    print(f"{YELLOW}  ЗАПРОС:{RESET}")
    print(f"  {WHITE}{ch['query']}{RESET}")
    print()
    print(f"{DIM_GREEN}  Подсказка: {ch['hint']}{RESET}")
    print()

    # Показываем варианты — один правильный, два ложных
    all_ops = ["OR", "AND", "UNION", "WHERE", "NOT", "HAVING", "LIKE", "IN"]
    correct_op = ch['answers'][0].upper()
    wrong_ops  = [op for op in all_ops if op != correct_op]
    import random as _r2
    options = _r2.sample(wrong_ops, 2) + [correct_op]
    _r2.shuffle(options)

    print(f"{DIM_GREEN}  Варианты операторов:{RESET}")
    for op in options:
        print(f"  {CYAN}  {op}{RESET}")
    print()

    try:
        answer = input(f"{BRIGHT_GREEN}  Введи оператор: {RESET}").strip()
    except (EOFError, KeyboardInterrupt):
        return dim("  Мини-игра прервана.")

    if answer.upper() in [a.upper() for a in ch['answers']]:
        state.add_trace(-25)
        if state.trace < 0:
            state.trace = 0
        state.add_xp(30)
        state.log("MINIGAME sql: WIN")
        return (
            f"{BRIGHT_GREEN}  ✔ ИНЪЕКЦИЯ УСПЕШНА!{RESET}\n"
            f"{DIM_GREEN}  {ch['explain']}{RESET}\n"
            f"{GREEN}  TRACE -25%  |  +30 XP{RESET}\n"
            + dim(f"  Текущий TRACE: {state.trace}%")
        )
    else:
        state.add_trace(10)
        correct = ch['answers'][0].upper()
        state.log(f"MINIGAME sql: FAIL got='{answer}' need='{correct}'")
        return (
            f"{RED}  ✘ НЕВЕРНО. Ответ: {WHITE}{correct}{RESET}\n"
            f"{DIM_GREEN}  {ch['explain']}{RESET}\n"
            + dim(f"  TRACE +10%. Текущий: {state.trace}%")
        )



def minigame_anagram(state) -> str:
    """
    ANAGRAM HACK — каждый раз случайное слово из встроенного списка.
    Угадай → открывает настоящий пароль и победа.
    Провал → TRACE +15%, пароль НЕ показывается.
    Даётся 3 попытки.
    """
    import random as _r

    # Список слов для анаграммы — независим от пароля игры
    _WORDS = [
        "access", "breach", "cipher", "daemon", "exploit",
        "filter", "ghost", "hacker", "inject", "kernel",
        "loader", "malware", "network", "output", "packet",
        "query", "rootkit", "socket", "tracer", "upload",
        "vector", "worm", "xploit", "zombie", "archive",
        "buffer", "crypto", "debug", "encode", "format",
        "gateway", "hidden", "image", "jumper", "keylog",
        "launch", "mirror", "nmap", "origin", "payload",
        "reboot", "signal", "tunnel", "unlock", "verify",
    ]

    pwd = _r.choice(_WORDS)

    # Перемешиваем буквы так чтобы не совпало с оригиналом
    letters = list(pwd)
    shuffled = letters[:]
    attempts_shuffle = 0
    while "".join(shuffled) == pwd and attempts_shuffle < 100:
        _r.shuffle(shuffled)
        attempts_shuffle += 1
    anagram = "".join(shuffled)

    print()
    scan_line("-", 54, YELLOW)
    slow_print(f"{YELLOW}  ▓▓ MINI-GAME: ANAGRAM HACK ▓▓{RESET}", delay=0.004)
    slow_print(f"{DIM_GREEN}  Буквы пароля перемешаны. Угадай — получишь пароль целиком.{RESET}", delay=0.004)
    scan_line("-", 54, YELLOW)
    print()
    print(f"{DIM_GREEN}  Перехвачен зашифрованный фрагмент памяти:{RESET}")
    print()

    # Показываем анаграмму красиво с пробелами
    spaced = "  ".join(f"{BRIGHT_GREEN}{BOLD}{c.upper()}{RESET}" for c in anagram)
    print(f"  {spaced}")
    print()
    print(f"{DIM_GREEN}  Букв в слове: {WHITE}{len(pwd)}{RESET}")
    print(f"{DIM_GREEN}  Подсказка: первая буква — {YELLOW}{pwd[0].upper()}{RESET}")
    print()

    max_tries = 3
    for attempt in range(1, max_tries + 1):
        print(f"{DIM_GREEN}  Попытка {attempt}/{max_tries}:{RESET}")
        try:
            answer = input(f"{BRIGHT_GREEN}  Введи слово: {RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return dim("  Мини-игра прервана.")

        if answer == pwd:
            # Победа — открываем букву которую ещё не открывали
            state.add_xp(50)
            state.log(f"MINIGAME anagram: WIN attempts={attempt} word={pwd}")
            real_pwd = state.password
            # Берём позиции которые ещё не открыты
            if not hasattr(state, "_anagram_revealed"):
                state._anagram_revealed = set()
            available = [i for i in range(len(real_pwd)) if i not in state._anagram_revealed]
            if not available:
                # Все буквы уже открыты
                return (
                    f"{BRIGHT_GREEN}  ✔ ВЕРНО! АНАГРАММА ВЗЛОМАНА!{RESET}\n"
                    f"{YELLOW}  Слово было: {WHITE}{BOLD}{pwd.upper()}{RESET}\n"
                    f"{DIM_GREEN}  Все буквы пароля уже открыты!{RESET}\n"
                    f"{GREEN}  +50 XP{RESET}\n"
                    + dim(f"  TRACE без изменений: {state.trace}%")
                )
            idx = _r.choice(available)
            state._anagram_revealed.add(idx)
            ch  = real_pwd[idx]
            masked = "".join(c if i in state._anagram_revealed else "░" for i, c in enumerate(real_pwd))
            return (
                f"{BRIGHT_GREEN}  ✔ ВЕРНО! АНАГРАММА ВЗЛОМАНА!{RESET}\n"
                f"\n"
                f"{YELLOW}  Слово было: {WHITE}{BOLD}{pwd.upper()}{RESET}\n"
                f"\n"
                f"{GREEN}  Фрагмент пароля NovaCorp получен:{RESET}\n"
                f"{YELLOW}  {masked}  [{idx}]='{ch}'{RESET}\n"
                f"{GREEN}  +50 XP  |  Открыто: {len(state._anagram_revealed)}/{len(real_pwd)}{RESET}\n"
                + dim(f"  TRACE без изменений: {state.trace}%")
            )

        # Неверно — только длину показываем, не слово
        correct_letters = sum(1 for a, b in zip(answer, pwd) if a == b)
        print(f"  {RED}  ✘ Неверно.{RESET}", end="")
        if len(answer) != len(pwd):
            print(f"  {DIM_GREEN}Длина неверная: нужно {len(pwd)} букв{RESET}")
        else:
            print(f"  {DIM_GREEN}Совпало на своих местах: {YELLOW}{correct_letters}/{len(pwd)}{RESET}")
        print()

    # Провал — показываем слово анаграммы, пароль игры не раскрываем
    state.add_trace(15)
    state.log("MINIGAME anagram: FAIL")
    return (
        f"{RED}  ✘ ПОПЫТКИ ИСЧЕРПАНЫ.{RESET}\n"
        f"{DIM_GREEN}  Слово было: {WHITE}{pwd.upper()}{RESET}\n"
        + dim(f"  TRACE +15%. Текущий: {state.trace}%")
    )