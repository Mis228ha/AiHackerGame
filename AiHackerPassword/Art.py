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

_SIMON_CHARS = list("ABCDEFGHJKLMNPQRSTUVWXYZ123456789!@#$%")

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

    sequence = random.sample(_SIMON_CHARS, rounds)  # уникальные символы
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



# ─── МИНИ-ИГРА: DATA STREAM INTERCEPTOR ─────────────────────────────────────

def minigame_datastream(state) -> str:
    """
    DATA STREAM INTERCEPTOR.

    Механика:
      - Печатаются строки потока одна за другой с паузой.
      - В случайную строку вставлен целевой символ пароля (подсвечен).
      - Игрок должен нажать Enter ПОКА символ виден на экране.
      - После символа поток идёт ещё несколько строк — если не нажал, пропуск.

    Управление:
      - Просто нажми Enter когда видишь подсвеченный символ.
      - Нажал раньше символа → ложное срабатывание.
      - Не нажал до конца потока → пропуск.

    Прогрессия:
      - Каждый раз открывается новая, ещё не открытая позиция пароля.
      - Скорость растёт с каждым успешным перехватом.
      - XP растёт с каждым следующим символом.
    """
    import sys as _sys
    import select as _select

    pwd = state.password

    # Позиции ещё не открытых символов
    if not hasattr(state, "_stream_revealed"):
        state._stream_revealed = set()

    available = [i for i in range(len(pwd)) if i not in state._stream_revealed]
    if not available:
        return dim("  Все символы пароля уже перехвачены. Используй /breach.")

    target_idx  = random.choice(available)
    target_char = pwd[target_idx]

    # Сложность: скорость растёт с каждым открытым символом
    revealed_count = len(state._stream_revealed)
    # Задержка между строками: от 0.55s (легко) до 0.22s (сложно)
    row_delay  = max(0.22, 0.55 - revealed_count * 0.05)
    # Сколько строк показывается ДО символа (окно реакции)
    pre_rows   = random.randint(5, 9)
    # Сколько строк символ остаётся видимым
    flash_rows = max(2, 4 - revealed_count // 2)
    # Строк после символа (ложная надежда)
    post_rows  = random.randint(3, 6)
    total_rows = pre_rows + flash_rows + post_rows

    COLS       = 52   # ширина строки потока
    _NOISE     = "0123456789ABCDEFabcdef><|/\\!@#$%^&*~+=[]{}?"

    def _noise_line() -> str:
        """Строка шума."""
        line = ""
        for _ in range(COLS):
            line += random.choice(_NOISE)
        return f"{DIM_GREEN}  {line}{RESET}"

    def _flash_line(char: str) -> str:
        """Строка с вспышкой целевого символа."""
        pos  = random.randint(4, COLS - 6)
        left = "".join(random.choice(_NOISE) for _ in range(pos))
        right= "".join(random.choice(_NOISE) for _ in range(COLS - pos - 3))
        return (f"{DIM_GREEN}  {left}"
                f"{BRIGHT_GREEN}{BOLD}[{char}]{RESET}"
                f"{DIM_GREEN}{right}{RESET}")

    # ── Шапка ────────────────────────────────────────────────────────────────
    print()
    scan_line("─", 56, BRIGHT_GREEN)
    slow_print(f"{BRIGHT_GREEN}  ▓▓ MINI-GAME: DATA STREAM INTERCEPTOR ▓▓{RESET}", delay=0.015)
    print(f"{DIM_GREEN}  Жди вспышку {BRIGHT_GREEN}[X]{DIM_GREEN} в потоке — жми {BRIGHT_GREEN}Enter{DIM_GREEN} когда видишь её.{RESET}")
    print(f"{DIM_GREEN}  Скорость: {'▓' * (revealed_count + 1)}{'░' * max(0, 6 - revealed_count - 1)}  "
          f"({row_delay*1000:.0f}ms/строку){RESET}")
    scan_line("─", 56, BRIGHT_GREEN)
    print()
    print(f"{YELLOW}  Готов? Нажми Enter для старта...{RESET}")

    try:
        input()
    except (KeyboardInterrupt, EOFError):
        return dim("  Мини-игра прервана.")

    # Очищаем буфер ввода перед стартом потока (важно для Windows)
    if _sys.platform == "win32":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getwch()

    # ── Поток ────────────────────────────────────────────────────────────────
    # Определяем в каких строках символ виден
    flash_start = pre_rows          # индекс первой строки с символом
    flash_end   = pre_rows + flash_rows - 1

    pressed_at  = None   # на какой строке нажали Enter
    aborted     = False

    def _nonblocking_check() -> bool:
        """
        True если Enter/Space нажаты прямо сейчас.
        Windows: msvcrt.kbhit() — работает в любом терминале/IDE.
        Unix:    select() с нулевым таймаутом.
        """
        try:
            if _sys.platform == "win32":
                import msvcrt
                # kbhit() не блокирует — возвращает True если есть символ
                if msvcrt.kbhit():
                    ch = msvcrt.getwch()
                    return ch in ("\r", "\n", " ")
                return False
            else:
                r, _, _ = _select.select([_sys.stdin], [], [], 0)
                if r:
                    _sys.stdin.readline()
                    return True
                return False
        except Exception:
            return False

    # Скрываем курсор на время игры
    print("\033[?25l", end="", flush=True)

    try:
        for row_idx in range(total_rows):
            in_flash = flash_start <= row_idx <= flash_end

            if in_flash:
                print(_flash_line(target_char), flush=True)
            else:
                print(_noise_line(), flush=True)

            time.sleep(row_delay)

            # Проверяем нажатие после каждой строки
            if _nonblocking_check() and pressed_at is None:
                pressed_at = row_idx
                # Показываем подтверждение и останавливаем поток
                print(f"{BRIGHT_GREEN}  >>> SPACE DETECTED <<<{RESET}", flush=True)
                break

    except (KeyboardInterrupt, EOFError):
        aborted = True
    finally:
        print("\033[?25h", end="", flush=True)  # возвращаем курсор

    print()

    if aborted:
        return dim("  Мини-игра прервана.")

    # ── Итог ─────────────────────────────────────────────────────────────────
    if pressed_at is None:
        # Не нажал до конца потока
        state.add_trace(12)
        state.log("MINIGAME datastream: MISS (no press)")
        return (
            f"{RED}  ✘ ПРОПУСК. Символ ушёл в поток.{RESET}\n"
            f"{DIM_GREEN}  Целевой символ был: {BRIGHT_GREEN}[{target_char}]{RESET}\n"
            + dim(f"  TRACE +12%. Текущий: {state.trace}%")
        )
    elif flash_start <= pressed_at <= flash_end:
        # Попал в окно
        state._stream_revealed.add(target_idx)
        masked = "".join(
            pwd[i] if i in state._stream_revealed else "░"
            for i in range(len(pwd))
        )
        xp_gain = 40 + revealed_count * 10
        state.add_xp(xp_gain)
        state.log(f"MINIGAME datastream: HIT pos={target_idx} char='{target_char}'")
        return (
            f"{BRIGHT_GREEN}  ✔ ПЕРЕХВАТ УСПЕШЕН!{RESET}\n"
            f"{GREEN}  Символ [{target_idx}] = '{BRIGHT_GREEN}{target_char}{GREEN}'{RESET}\n"
            f"{YELLOW}  {masked}{RESET}\n"
            + dim(f"  +{xp_gain} XP  |  Открыто: {len(state._stream_revealed)}/{len(pwd)}")
        )
    else:
        # Нажал слишком рано
        state.add_trace(12)
        state.log("MINIGAME datastream: FALSE (too early)")
        return (
            f"{RED}  ✘ СЛИШКОМ РАНО. Ложное срабатывание.{RESET}\n"
            f"{DIM_GREEN}  Символ ещё не появился в строке {pressed_at + 1}, "
            f"а должен был в строке {flash_start + 1}.{RESET}\n"
            + dim(f"  TRACE +12%. Текущий: {state.trace}%")
        )





# ─── МИНИ-ИГРА: CRC CHECK ────────────────────────────────────────────────────

def minigame_crc(state) -> str:
    """
    CRC CHECK — живой обратный отсчёт + посимвольный ввод.
    Лёгкий: 30 сек | Средний: 20 сек | Сложный: 10 сек
    Время вышло → сразу завершается, TRACE +8%.
    Успех → TRACE -20%.
    """
    import sys as _sys
    import time as _time
    import threading as _threading

    time_limits = {"easy": 30, "medium": 20, "hard": 10}
    time_limit  = time_limits.get(state.difficulty, 20)

    a = random.randint(1, 99)
    b = random.randint(1, 99)
    c = random.randint(1, 99)
    correct = a + b + c

    print()
    scan_line("─", 56, YELLOW)
    slow_print(f"{YELLOW}  ▓▓ MINI-GAME: CRC CHECKSUM VERIFICATION ▓▓{RESET}", delay=0.012)
    print(f"{DIM_GREEN}  Реши пример пока не истекло время. Введи сумму + Enter.{RESET}")
    print(f"{DIM_GREEN}  Успех: TRACE {GREEN}-20%{DIM_GREEN}  |  Провал: TRACE {RED}+8%{RESET}")
    diff_labels = {
        "easy":   f"{GREEN}  [EASY]   30 сек  ●──────────────{RESET}",
        "medium": f"{YELLOW}  [MEDIUM] 20 сек  ●─────────{RESET}",
        "hard":   f"{RED}  [HARD]   10 сек  ●────{RESET}",
    }
    print(diff_labels.get(state.difficulty, ""))
    scan_line("─", 56, YELLOW)
    print()
    print(f"{BRIGHT_GREEN}  CRC CHECK:  {WHITE}{a}  +  {b}  +  {c}  = ?{RESET}")
    print()

    # Разделяемое состояние
    chars      = []
    timed_out  = [False]
    stop       = _threading.Event()

    # ── Поток обратного отсчёта ───────────────────────────────────────────────
    def _countdown():
        t0 = _time.time()
        while not stop.is_set():
            remaining = time_limit - (_time.time() - t0)
            if remaining <= 0:
                timed_out[0] = True
                stop.set()
                break
            bar_len = 20
            filled  = int((remaining / time_limit) * bar_len)
            if remaining > time_limit * 0.5:
                col = GREEN
            elif remaining > time_limit * 0.2:
                col = YELLOW
            else:
                col = RED
            bar   = col + "█" * filled + "░" * (bar_len - filled) + RESET
            typed = "".join(chars)
            print(f"\r  {bar} {col}{remaining:5.1f}s{RESET}  > {BRIGHT_GREEN}{typed}{RESET}   ",
                  end="", flush=True)
            _time.sleep(0.1)
        # Стираем строку таймера
        print(f"\r{' ' * 60}\r", end="", flush=True)

    t = _threading.Thread(target=_countdown, daemon=True)
    t.start()

    # ── Ввод: Windows (msvcrt) / Unix (termios) ───────────────────────────────
    if _sys.platform == "win32":
        import msvcrt as _msvcrt
        while not stop.is_set():
            if _msvcrt.kbhit():
                ch = _msvcrt.getwch()
                if ch in ("\r", "\n"):
                    stop.set()
                    break
                elif ch in ("\x08", "\x7f"):
                    if chars:
                        chars.pop()
                elif ch.isdigit() or (ch == "-" and not chars):
                    chars.append(ch)
            _time.sleep(0.02)
    else:
        import tty as _tty, termios as _termios, select as _sel
        fd  = _sys.stdin.fileno()
        old = _termios.tcgetattr(fd)
        try:
            _tty.setraw(fd)
            while not stop.is_set():
                rlist, _, _ = _sel.select([_sys.stdin], [], [], 0.05)
                if rlist:
                    ch = _sys.stdin.read(1)
                    if ch in ("\r", "\n"):
                        stop.set()
                        break
                    elif ch in ("\x08", "\x7f"):
                        if chars:
                            chars.pop()
                    elif ch.isdigit() or (ch == "-" and not chars):
                        chars.append(ch)
        finally:
            _termios.tcsetattr(fd, _termios.TCSADRAIN, old)

    stop.set()
    t.join(timeout=0.5)
    print()

    # ── Результат ─────────────────────────────────────────────────────────────
    if timed_out[0]:
        state.add_trace(8)
        state.log(f"MINIGAME crc: TIMEOUT limit={time_limit}s")
        return (
            f"{RED}  ✘ ВРЕМЯ ВЫШЛО! Лимит {time_limit} сек исчерпан.{RESET}\n"
            f"{DIM_GREEN}  Верный ответ был: {WHITE}{correct}{RESET}\n"
            + dim(f"  TRACE +8%. Текущий: {state.trace}%")
        )

    answer_str = "".join(chars).strip()
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

    # Победа
    reduction = min(state.trace, 20)
    state.trace = max(0, state.trace - 20)
    state.add_xp(20)
    state.log("MINIGAME crc: WIN")
    bonus = ""
    if len(answer_str) <= 3:
        state.add_xp(10)
        bonus = f"\n{BRIGHT_GREEN}  ⚡ БЫСТРО! +10 XP бонус{RESET}"
    return (
        f"{BRIGHT_GREEN}  ✔ ВЕРИФИКАЦИЯ ПРОЙДЕНА!  {a} + {b} + {c} = {correct}{RESET}\n"
        f"{GREEN}  TRACE -{reduction}%  |  +20 XP{RESET}"
        + bonus + "\n"
        + dim(f"  Текущий TRACE: {state.trace}%")
    )