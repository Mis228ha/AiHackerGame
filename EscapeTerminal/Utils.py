import os, sys, re, time, threading

# --- WINDOWS UTF-8 FIX --------------------------------------------------------
if os.name == "nt":
    import ctypes
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    ctypes.windll.kernel32.SetConsoleCP(65001)
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1, closefd=False)
    sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1, closefd=False)
    sys.stdin  = open(sys.stdin.fileno(),  mode='r', encoding='utf-8', buffering=1, closefd=False)

# --- ЦВЕТА --------------------------------------------------------------------
G  = "\033[92m";  BG = "\033[1;92m"; DG = "\033[2;32m"
R  = "\033[91m";  Y  = "\033[93m";   C  = "\033[96m"
W  = "\033[97m";  M  = "\033[95m";   B  = "\033[94m"
DM = "\033[2m";   BD = "\033[1m";    RS = "\033[0m"

# --- БАЗОВЫЕ УТИЛИТЫ ----------------------------------------------------------
def safe_input(prompt=""):
    try:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        line = sys.stdin.readline()
        if line == "": return ""
        return line.rstrip("\n").rstrip("\r")
    except (UnicodeDecodeError, UnicodeEncodeError, KeyboardInterrupt, EOFError):
        return ""

def clr():
    os.system("clear" if os.name != "nt" else "cls")

def slow(text, d=0.015):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(d)
    print()

def line(ch="-", n=60, col=DG):
    print(f"{col}{ch*n}{RS}")

def pause(msg=None):
    if msg is None:
        msg = f"\n{Y}  >> Нажми Enter чтобы продолжить{RS}"
    safe_input(msg + "\n")

def strip_ansi(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)

# --- ЭКРАНЫ ПОБЕДЫ / ПОРАЖЕНИЯ -----------------------------------------------
def win_screen(title, score, detail=""):
    print()
    line("=", 60, BG)
    slow(f"{BG}  [OK]  ПОБЕДА: {title}{RS}", 0.015)
    line("-", 60, DG)
    if detail:
        print(f"{G}  {detail}{RS}")
    print(f"{Y}  ОЧКИ: {BD}+{score}{RS}")
    line("=", 60, BG)

def lose_screen(title, reason="", hint=""):
    print()
    line("=", 60, R)
    slow(f"{R}  [XX]  ПРОВАЛ: {title}{RS}", 0.015)
    line("-", 60, DG)
    if reason:
        print(f"{R}  Причина: {reason}{RS}")
    if hint:
        print(f"{DG}  Подсказка: {hint}{RS}")
    line("=", 60, R)

# --- ТАЙМЕР -------------------------------------------------------------------
def timed_input(prompt, time_limit):
    result = [None]
    answered = threading.Event()

    def _bar(left):
        col   = G if left > time_limit * 0.5 else (Y if left > time_limit * 0.2 else R)
        bar_n = max(0, int((left / time_limit) * 20))
        bar   = "#" * bar_n + "." * (20 - bar_n)
        return f"  {col}[T] [{bar}] {left:.0f}s осталось{RS}"

    print(_bar(time_limit))

    def read_it():
        try:
            result[0] = safe_input(prompt)
        except (KeyboardInterrupt, EOFError):
            result[0] = ""
        answered.set()

    start = time.time()
    th = threading.Thread(target=read_it, daemon=True)
    th.start()

    def timer_tick():
        tick = 1
        while not answered.is_set():
            time.sleep(0.25)
            elapsed_t = time.time() - start
            left_t    = time_limit - elapsed_t
            if left_t <= 0: break
            if int(elapsed_t) > 0 and int(elapsed_t) % 5 == 0 and int(elapsed_t) // 5 >= tick:
                tick = int(elapsed_t) // 5 + 1
                sys.stdout.write("\n" + _bar(left_t) + "\n")
                sys.stdout.flush()

    tt = threading.Thread(target=timer_tick, daemon=True)
    tt.start()
    answered.wait(timeout=time_limit + 1.0)
    elapsed = time.time() - start
    if result[0] is None:
        return None, elapsed
    return result[0].strip(), elapsed