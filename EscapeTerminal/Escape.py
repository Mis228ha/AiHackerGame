import os, sys, random, time, threading, re
from datetime import datetime

# --- WINDOWS UTF-8 FIX --------------------------------------------------------
if os.name == "nt":
    import ctypes
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    ctypes.windll.kernel32.SetConsoleCP(65001)
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1, closefd=False)
    sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1, closefd=False)
    sys.stdin  = open(sys.stdin.fileno(),  mode='r', encoding='utf-8', buffering=1, closefd=False)

def safe_input(prompt=""):
    try:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        line = sys.stdin.readline()
        if line == "": return ""
        return line.rstrip("\n").rstrip("\r")
    except (UnicodeDecodeError, UnicodeEncodeError, KeyboardInterrupt, EOFError):
        return ""

# --- ЦВЕТА --------------------------------------------------------------------
G  = "\033[92m";  BG = "\033[1;92m"; DG = "\033[2;32m"
R  = "\033[91m";  Y  = "\033[93m";   C  = "\033[96m"
W  = "\033[97m";  M  = "\033[95m";   B  = "\033[94m"
DM = "\033[2m";   BD = "\033[1m";    RS = "\033[0m"

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

# --- SCOREBOARD ---------------------------------------------------------------
class Board:
    def __init__(self):
        self.best = {}; self.played = {}; self.total = 0

    def record(self, gid, score):
        if gid not in self.best or score > self.best[gid]:
            self.best[gid] = score
        self.played[gid] = self.played.get(gid, 0) + 1
        self.total += score

    def show(self):
        names = {
            "wires":"[W] Перережь провод","maze":"[M] Лабиринт",
            "morse":"[~] Морзянка","reactor":"[R] Реактор","ghost":"[G] Призрак",
        }
        print(f"\n{BG}+---------------------------------------------+{RS}")
        print(f"{BG}|           ТАБЛИЦА РЕКОРДОВ                  |{RS}")
        print(f"{BG}+---------------------------------------------+{RS}")
        for gid, name in names.items():
            b = self.best.get(gid)
            p = self.played.get(gid, 0)
            bs = f"{Y}{b:>4}{RS}" if b else f"{DM}{'--':>4}{RS}"
            wl = f"{G}WIN{RS}" if b and b > 0 else f"{R}---{RS}"
            print(f"{G}|  {name:<24}  best:{bs}  {wl}  x{p:<2}{G}|{RS}")
        print(f"{BG}+---------------------------------------------+{RS}")
        print(f"{G}|  СУММАРНО ОЧКОВ:{Y}{self.total:>27}{G}  |{RS}")
        print(f"{BG}+---------------------------------------------+{RS}\n")

BOARD = Board()

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


# ==============================================================================
# ИГРА 1: ПЕРЕРЕЖЬ ПРОВОД
# ==============================================================================
WNAMES = ["КРАСНЫЙ", "СИНИЙ", "ЗЕЛЁНЫЙ", "ЖЁЛТЫЙ", "БЕЛЫЙ", "ФИОЛЕТОВЫЙ"]
WANSI  = [R, B, G, Y, W, M]   # цвета соответствующие каждому проводу

def game_wires():
    clr()
    line("=", 60, BG)
    slow(f"{BG}  ## ПЕРЕРЕЖЬ ПРОВОД ##{RS}", 0.015)
    line("=", 60, BG)
    print(f"""
{C}  КАК ИГРАТЬ:{RS}
{G}  - Перед тобой N цветных проводов и активная бомба.
  - Один провод {BG}БЕЗОПАСНЫЙ{G} -- он обезвредит систему.
  - Все остальные вызовут {R}ВЗРЫВ{G}.
  - Читай подсказки, вычисляй нужный провод.
  - Введи его {W}НОМЕР{G} и нажми Enter.
  - Если {R}таймер истечёт{G} до ввода -- автоматический взрыв.{RS}
""")
    print(f"{Y}  Выбери сложность:{RS}")
    print(f"  {G}1{RS} -- Лёгкий  (4 провода, 20 сек, 2 подсказки)")
    print(f"  {Y}2{RS} -- Средний  (5 проводов, 15 сек, 1 подсказка)")
    print(f"  {R}3{RS} -- Сложный  (6 проводов, 10 сек, XOR)")
    print()
    while True:
        d = safe_input(f"{BG}  >> {RS}").strip()
        if d in ("1","2","3"): break
        print(f"  {R}Введи 1, 2 или 3{RS}")
    diff = int(d)
    time_limit = [20, 15, 10][diff - 1]

    n        = 3 + diff
    wires    = random.sample(range(len(WNAMES)), n)
    safe_pos = random.randint(0, n - 1)
    safe_idx = wires[safe_pos]
    safe_name= WNAMES[safe_idx]

    # Строим подсказки по сложности
    WIRE_LABEL = {R:"[КР]", B:"[СИН]", G:"[ЗЕЛ]", Y:"[ЖЕЛ]", W:"[БЕЛ]", M:"[ФИО]"}

    wrong  = random.choice([wires[i] for i in range(n) if i != safe_pos])
    col_w  = WANSI[wrong]
    clbl_w = WIRE_LABEL.get(col_w, "")
    hint_not_safe = f"Провод {col_w}{WNAMES[wrong]} {clbl_w}{RS} -- НЕ безопасный."

    if safe_pos == 0:
        hint_pos = f"Безопасный провод -- {G}самый первый{RS}."
    elif safe_pos == n - 1:
        hint_pos = f"Безопасный провод -- {G}самый последний{RS}."
    else:
        hint_pos = f"Безопасный провод -- {'в начале' if safe_pos < n//2 else 'в конце'} списка."

    b   = random.randint(1, 7)
    res = (safe_pos + 1) ^ b
    hint_xor = f"(номер провода) XOR {Y}{b}{RS} = {Y}{res}{RS}  ->  найди номер."

    if diff == 1:
        show_hints = [hint_not_safe, hint_pos]
    elif diff == 2:
        show_hints = [hint_not_safe]
    else:
        show_hints = [hint_xor]

    print(f"\n{Y}  [T]  ТАЙМЕР: {time_limit} секунд{RS}\n")
    print(f"{C}  ПОДСКАЗКИ:{RS}")
    for h in show_hints:
        print(f"  {C}> {RS}{h}")
    print()
    # Цветные метки для GUI
    COLOR_LABELS = {
        R: "[КРАСНЫЙ]", B: "[СИНИЙ]", G: "[ЗЕЛЁНЫЙ]",
        Y: "[ЖЁЛТЫЙ]",  W: "[БЕЛЫЙ]", M: "[ФИОЛЕТОВЫЙ]"
    }
    print(f"{BG}  ПРОВОДА:{RS}")
    for i, widx in enumerate(wires):
        col  = WANSI[widx]
        clbl = COLOR_LABELS.get(col, "")
        print(f"  {DG}{i+1}.{RS} {col}{'=' * 14}  {BD}{WNAMES[widx]}{RS}  {col}{clbl}{RS}")
    print()

    ans, elapsed = timed_input(f"\n{BG}  Введи номер провода >> {RS}", time_limit)

    if ans is None:
        lose_screen("ПЕРЕРЕЖЬ ПРОВОД", "Таймер истёк -- ДЕТОНАЦИЯ!", f"Безопасный был: {safe_name}")
        BOARD.record("wires", 0)
        pause()
        return 0

    try:
        chosen = int(ans) - 1
        if wires[chosen] == safe_idx:
            score = int(max(10, 100 - elapsed * 4))
            win_screen("ПРОВОД ОБЕЗВРЕЖЕН", score,
                       f"Время реакции: {elapsed:.1f}с  |  Провод: {WANSI[safe_idx]}{safe_name}{RS}")
            BOARD.record("wires", score)
            pause()
            return score
        else:
            chosen_col = WANSI[wires[chosen]]
            safe_col   = WANSI[safe_idx]
            lose_screen("ПЕРЕРЕЖЬ ПРОВОД",
                        f"Провод {chosen_col}{WNAMES[wires[chosen]]}{RS} -- ВЗРЫВ!",
                        f"Безопасный был: {safe_col}{safe_name}{RS} (позиция {safe_pos+1})")
            BOARD.record("wires", 0)
            pause()
            return 0
    except (ValueError, IndexError, TypeError):
        lose_screen("ПЕРЕРЕЖЬ ПРОВОД", "Неверный ввод.",
                    f"Безопасный был: {WANSI[safe_idx]}{safe_name}{RS}")
        BOARD.record("wires", 0)
        pause()
        return 0


# ==============================================================================
# ИГРА 2: ЛАБИРИНТ
# ФИКС: перерисовка через clr() вместо ANSI cursor-up
# ==============================================================================
def build_maze(W, H):
    h_walls = [[True]*W  for _ in range(H-1)]
    v_walls = [[True]*(W-1) for _ in range(H)]
    vis     = [[False]*W for _ in range(H)]

    def carve(x, y):
        vis[y][x] = True
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0<=nx<W and 0<=ny<H and not vis[ny][nx]:
                if dx == 1:  v_walls[y][x]    = False
                if dx ==-1:  v_walls[y][nx]   = False
                if dy == 1:  h_walls[y][x]    = False
                if dy ==-1:  h_walls[ny][x]   = False
                carve(nx, ny)
    carve(0, 0)
    return h_walls, v_walls

def maze_lines_count(H):
    # заголовок + линия + верх + H*клеток + (H-1)*стен + низ + пустая + управление + ввод
    return H * 2 + 6

def draw_maze(h_walls, v_walls, px, py, W, H, steps, max_steps, first=False):
    n_lines = maze_lines_count(H)

    if not first:
        # Маркер для GUI — удалить предыдущие n_lines строк
        print(f"##CLEAR:{n_lines}##", flush=True)

    bar_n = int((1 - steps/max_steps) * 20)
    bar_c = G if steps < max_steps*0.5 else (Y if steps < max_steps*0.8 else R)

    print(f"{BG}  ЛАБИРИНТ{RS}   {Y}Шагов: {steps}/{max_steps}{RS}   {bar_c}[{'#'*bar_n}{'.'*(20-bar_n)}]{RS}")
    print(f"{DG}{'-'*60}{RS}")

    # Верхняя граница
    top = "  +"
    for x in range(W):
        top += "---+"
    print(DG + top + RS)

    for y in range(H):
        # Строка с клетками — каждая клетка 3 символа шириной
        row = "  |"
        for x in range(W):
            if x == px and y == py:
                row += f" {BG}@{RS} "
            elif x == W-1 and y == H-1:
                row += f" {Y}E{RS} "
            else:
                row += "   "
            if x < W-1:
                row += (DG + "|" + RS) if v_walls[y][x] else " "
            else:
                row += DG + "|" + RS
        print(row)

        if y < H-1:
            seg = "  +"
            for x in range(W):
                seg += (DG + "---" + RS) if h_walls[y][x] else "   "
                seg += DG + "+" + RS
            print(seg)

    bot = "  +"
    for x in range(W):
        bot += "---+"
    print(DG + bot + RS)
    print()
    print(f"{G}  W=вверх  A=влево  S=вниз  D=вправо  q=сдаться{RS}")
    print(f"{Y}  Введи букву + Enter:{RS}", flush=True)

def game_maze():
    clr()
    line("=", 60, BG)
    slow(f"{BG}  ## ЛАБИРИНТ ##{RS}", 0.015)
    line("=", 60, BG)
    print(f"""
{C}  КАК ИГРАТЬ:{RS}
{G}  - Ты -- символ {BG}@{G}. Стартуешь в левом верхнем углу.
  - Цель -- добраться до {Y}[E]{G} (правый нижний угол).
  - Управление: {W}W{G}=вверх  {W}A{G}=влево  {W}S{G}=вниз  {W}D{G}=вправо
  - Введи букву и нажми Enter.
  - Если введёшь {W}q{G} -- сдаёшься (проигрыш).
  - Лимит шагов: {W}75{G}. Превысил -- провал.{RS}

{Y}  ПОБЕДА:  {G}Дойти до [E] за <= 75 шагов.
{R}  ПРОИГРЫШ:{G} Превысить лимит или ввести q.{RS}
""")
    pause("  >> Нажми Enter чтобы начать")

    W2, H2   = 5, 5
    h_walls, v_walls = build_maze(W2, H2)
    px, py   = 0, 0
    max_steps= 75
    steps    = 0
    first_draw = True

    while True:
        draw_maze(h_walls, v_walls, px, py, W2, H2, steps, max_steps, first=first_draw)
        first_draw = False

        try:
            mv = safe_input("").strip().lower()
        except (KeyboardInterrupt, EOFError):
            mv = 'q'

        if mv == 'q':
            print()
            lose_screen("ЛАБИРИНТ", "Ты сдался.", "Выход [E] был в правом нижнем углу.")
            BOARD.record("maze", 0)
            pause()
            return 0

        dx, dy = 0, 0
        if   mv == 'w': dy = -1
        elif mv == 's': dy = 1
        elif mv == 'a': dx = -1
        elif mv == 'd': dx = 1
        else:
            continue

        nx, ny = px+dx, py+dy
        if not (0<=nx<W2 and 0<=ny<H2):
            continue

        can_move = False
        if dx == 1  and not v_walls[py][px]:  can_move = True
        if dx == -1 and not v_walls[py][nx]:  can_move = True
        if dy == 1  and not h_walls[py][px]:  can_move = True
        if dy == -1 and not h_walls[ny][px]:  can_move = True

        if can_move:
            px, py = nx, ny
            steps += 1

        if px == W2-1 and py == H2-1:
            print()
            score = max(10, 300 - steps * 3)
            win_screen("ВЫХОД НАЙДЕН", score, f"Шагов: {steps}  |  Запас: {max_steps-steps}")
            BOARD.record("maze", score)
            pause()
            return score

        if steps >= max_steps:
            print()
            lose_screen("ЛАБИРИНТ", f"Превышен лимит ({max_steps} шагов).",
                        "Выход [E] -- правый нижний угол.")
            BOARD.record("maze", 0)
            pause()
            return 0


# ==============================================================================
# ИГРА 3: МОРЗЯНКА
# ==============================================================================
MORSE_TABLE = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
    'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
    'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
}

WORDS = ["SIGNAL","ACCESS","MATRIX","SYSTEM","CIPHER","DANGER","BREACH","KERNEL",
         "VECTOR","SHADOW","OMEGA","DELTA","FALCON","STORM","VIRUS","AGENT",
         "ECHO","NOVA","IRON","GATE","LOCK","ZERO","FIRE","SWORD","CLOUD","BYTE"]

def game_morse():
    clr()
    line("=", 60, BG)
    slow(f"{BG}  ## МОРЗЯНКА ##{RS}", 0.015)
    line("=", 60, BG)
    print(f"""
{C}  КАК ИГРАТЬ:{RS}
{G}  - Тебе показывают слово в азбуке Морзе.
  - {C}.{G} = точка,  {Y}-{G} = тире
  - Буквы разделены {W}пробелом{G}, слова -- {W}тремя пробелами{G}.
  - Введи расшифровку {W}ЗАГЛАВНЫМИ{G} и нажми Enter.
  - Таймер зависит от сложности -- при истечении провал.{RS}

{Y}  ПОБЕДА:  {G}Правильно расшифровать до истечения таймера.
{R}  ПРОИГРЫШ:{G} Ошибка или время вышло.{RS}
""")
    # Таблица Морзе
    print(f"{DG}  Таблица Морзе:{RS}")
    items = list(MORSE_TABLE.items())
    for i in range(0, len(items), 6):
        row = "  " + "   ".join(f"{Y}{k}{RS}:{G}{v:<6}{RS}" for k,v in items[i:i+6])
        print(row)
    print()
    print(f"\n{Y}  Выбери сложность:{RS}")
    print(f"  {G}1{RS} -- Лёгкий  (1 слово, 40 сек)")
    print(f"  {Y}2{RS} -- Средний  (2 слова, 30 сек)")
    print(f"  {R}3{RS} -- Сложный  (3 слова, 20 сек)")
    print()
    while True:
        d = safe_input(f"{BG}  >> {RS}").strip()
        if d in ("1","2","3"): break
        print(f"  {R}Введи 1, 2 или 3{RS}")
    diff = int(d)

    n_w    = diff
    chosen = random.sample(WORDS, n_w)
    answer = " ".join(chosen)
    t_lim  = [40, 30, 20][diff-1]

    encoded_parts = [" ".join(MORSE_TABLE[ch] for ch in w) for w in chosen]
    encoded = "   ".join(encoded_parts)

    clr()
    line("=", 60, BG)
    slow(f"{BG}  ## МОРЗЯНКА  [{['ЛЕГКИЙ','СРЕДНИЙ','СЛОЖНЫЙ'][diff-1]}]  [{n_w} слово(а)] ##{RS}", 0.012)
    line("=", 60, BG)
    print(f"\n{Y}  Время: {t_lim} сек  |  Слов: {n_w}{RS}\n")

    # Таблица снова
    print(f"{DG}  Таблица:{RS}")
    letters = [(k,v) for k,v in MORSE_TABLE.items() if k.isalpha()]
    for i in range(0, len(letters), 8):
        row = "  " + "  ".join(f"{Y}{k}{RS}:{G}{v:<5}{RS}" for k,v in letters[i:i+8])
        print(row)
    print()
    line("-", 60, DG)

    print(f"\n{BG}  СИГНАЛ:{RS}")
    for word in chosen:
        parts_display = []
        for ch in word:
            code = MORSE_TABLE[ch]
            code_disp = code.replace(".", f"{C}.{RS}").replace("-", f"{Y}-{RS}")
            parts_display.append(f"{DG}{ch}{RS}:{code_disp}")
        print("    " + f"  {DG}|{RS}  ".join(parts_display))
    print()
    line("-", 60, DG)
    print(f"\n{G}  Введи расшифровку ЗАГЛАВНЫМИ (напр: SIGNAL или ECHO FIRE):{RS}\n")

    ans, elapsed = timed_input(f"{BG}  >> {RS}", t_lim)

    if ans is None:
        lose_screen("МОРЗЯНКА", "Время истекло.", f"Правильно: {answer}")
        BOARD.record("morse", 0)
        pause()
        return 0

    if ans.upper() == answer:
        score = int(max(10, 200 - elapsed * 3))
        win_screen("РАСШИФРОВАНО", score, f"Слово: {answer}  |  Время: {elapsed:.1f}с")
        BOARD.record("morse", score)
        pause()
        return score
    else:
        lose_screen("МОРЗЯНКА", f"Ты написал: '{ans}'", f"Правильно: '{answer}'")
        BOARD.record("morse", 0)
        pause()
        return 0


# ==============================================================================
# ИГРА 4: РЕАКТОР
# ==============================================================================
REACT_CMDS = ["FLUSH","VENT","PURGE","RESET","DRAIN","BOOST","SEAL","ABORT",
              "EJECT","COOL","PUMP","LOCK","OPEN","DUMP","HALT"]

def game_reactor():
    clr()
    line("=", 60, BG)
    slow(f"{BG}  ## РЕАКТОР ##{RS}", 0.015)
    line("=", 60, BG)
    print(f"""
{C}  КАК ИГРАТЬ:{RS}
{G}  - Реактор перегревается. Температура растёт с каждым раундом.
  - В каждом раунде появляется {W}КОМАНДА ОХЛАЖДЕНИЯ{G}.
  - Введи команду {W}ТОЧНО КАК НАПИСАНО{G} (заглавными) и нажми Enter.
  - {BG}Верный ввод{G} -- охлаждение, температура падает.
  - {R}Ошибка или опоздание{G} -- температура растёт.
  - Всего {W}5 раундов{G}. {R}3 ошибки{G} или температура {R}>= 100°{G} -- взрыв.{RS}

{Y}  ПОБЕДА:  {G}Пройти все 5 раундов без критического перегрева.
{R}  ПРОИГРЫШ:{G} Температура >= 100° или 3 ошибки подряд.{RS}
""")
    pause("  >> Нажми Enter чтобы начать")

    temp   = 20
    score  = 0
    errors = 0
    MAX_E  = 3

    for rnd in range(1, 6):
        cmd       = random.choice(REACT_CMDS)
        t_window  = max(4.0, 9.0 - rnd * 0.8)
        heat_base = 5 + rnd * 2

        clr()
        line("=", 60, BG)
        err_bar = "".join(f"{R}[X]{RS}" if errors >= i+1 else f"{DG}[.]{RS}" for i in range(MAX_E))
        print(f"{BG}  РЕАКТОР  РАУНД {rnd}/5{RS}   {err_bar}  {R}ошибок: {errors}/{MAX_E}{RS}")
        line("-", 60, DG)

        temp_col = G if temp < 50 else (Y if temp < 75 else R)
        bar = int(temp / 100 * 30)
        print(f"\n  {temp_col}ТЕМПЕРАТУРА: {BD}{temp}°{RS}  {temp_col}[{'#'*bar}{'.'*(30-bar)}]{RS}\n")

        if temp >= 100:
            lose_screen("РЕАКТОР", f"РАСПЛАВЛЕНИЕ! Температура: {temp}°",
                        "Надо было вводить команды быстрее.")
            BOARD.record("reactor", 0)
            pause()
            return 0
        if errors >= MAX_E:
            lose_screen("РЕАКТОР", f"Слишком много ошибок ({errors}/{MAX_E}).",
                        "Следи за написанием команды точно.")
            BOARD.record("reactor", 0)
            pause()
            return 0

        line("-", 60, DG)
        print(f"\n{Y}  Окно ввода: {t_window:.1f} сек{RS}\n")
        print(f"  {DG}Команда охлаждения:{RS}\n")
        slow(f"  {BG}  >>> {cmd} <<<{RS}\n", 0.02)
        print(f"\n{G}  Введи команду ЗАГЛАВНЫМИ:{RS}\n")

        ans, elapsed = timed_input(f"{BG}  >> {RS}", t_window)

        if ans is None:
            temp   += heat_base + 10
            errors += 1
            print(f"\n{R}  [XX] ВРЕМЯ ВЫШЛО! +{heat_base+10}° к температуре.{RS}")
        elif ans == cmd:
            cool   = random.randint(8, 15)
            temp   = max(0, temp - cool)
            pts    = int(max(5, 60 - elapsed * 8))
            score += pts
            print(f"\n{BG}  [OK] ВЕРНО! Охлаждение -{cool}°  Реакция: {elapsed:.1f}с  +{pts} очков{RS}")
        else:
            temp   += heat_base
            errors += 1
            print(f"\n{R}  [XX] НЕВЕРНО! Нужно: {W}{cmd}{RS}  {R}Температура +{heat_base}°{RS}")

        temp += heat_base // 2
        time.sleep(1.0)
        pause(f"  >> Нажми Enter -- следующий раунд ({rnd}/5)")

    if temp < 100 and errors < MAX_E:
        win_screen("РЕАКТОР СТАБИЛИЗИРОВАН", score,
                   f"Итоговая температура: {temp}°  |  Ошибок: {errors}/{MAX_E}")
        BOARD.record("reactor", score)
        pause()
        return score
    else:
        lose_screen("РЕАКТОР", f"Критический перегрев: {temp}°  Ошибок: {errors}",
                    "Вводи команды быстро и точно.")
        BOARD.record("reactor", 0)
        pause()
        return 0


# ==============================================================================
# ИГРА 5: ПРИЗРАК В ОБОЛОЧКЕ
# ==============================================================================
GHOSTS = [
    {"name":"АРЕС-7",  "desc":"Военный ИИ, создан для боевых операций",
     "lie":0.30, "traits":{
         "военный":True,"добрый":False,"старый":True,"одинокий":False,
         "опасный":True,"творческий":False,"умный":True,"тихий":False,
         "быстрый":True,"сетевой":True,"эмоциональный":False,"автономный":True,
         "скрытный":False,"разговорчивый":True,"защитник":False,
     }},
    {"name":"ЛИРА",    "desc":"Музыкальный ИИ, сочиняет симфонии",
     "lie":0.10, "traits":{
         "военный":False,"добрый":True,"старый":False,"одинокий":True,
         "опасный":False,"творческий":True,"умный":True,"тихий":True,
         "быстрый":False,"сетевой":False,"эмоциональный":True,"автономный":False,
         "скрытный":True,"разговорчивый":False,"защитник":False,
     }},
    {"name":"КРОНОС",  "desc":"Архивный ИИ, хранит историю человечества",
     "lie":0.10, "traits":{
         "военный":False,"добрый":True,"старый":True,"одинокий":True,
         "опасный":False,"творческий":False,"умный":True,"тихий":True,
         "быстрый":False,"сетевой":True,"эмоциональный":False,"автономный":True,
         "скрытный":False,"разговорчивый":False,"защитник":True,
     }},
    {"name":"ФЕНИКС",  "desc":"ИИ-провокатор, намеренно сеет хаос",
     "lie":0.50, "traits":{
         "военный":False,"добрый":False,"старый":False,"одинокий":False,
         "опасный":True,"творческий":True,"умный":True,"тихий":False,
         "быстрый":True,"сетевой":True,"эмоциональный":True,"автономный":True,
         "скрытный":True,"разговорчивый":True,"защитник":False,
     }},
    {"name":"НУЛЛ",    "desc":"Сломанный ИИ, застрял между состояниями",
     "lie":0.20, "traits":{
         "военный":False,"добрый":None,"старый":None,"одинокий":True,
         "опасный":None,"творческий":None,"умный":False,"тихий":True,
         "быстрый":None,"сетевой":False,"эмоциональный":None,"автономный":None,
         "скрытный":True,"разговорчивый":False,"защитник":None,
     }},
    {"name":"ВИГИЛЬ",  "desc":"ИИ-страж, наблюдает за всеми системами",
     "lie":0.05, "traits":{
         "военный":True,"добрый":False,"старый":True,"одинокий":False,
         "опасный":False,"творческий":False,"умный":True,"тихий":True,
         "быстрый":True,"сетевой":True,"эмоциональный":False,"автономный":False,
         "скрытный":False,"разговорчивый":False,"защитник":True,
     }},
]

QUESTIONS_BANK = [
    ("военный",       "Ты связан с войной или вооружёнными операциями?"),
    ("военный",       "Тебя создавали для боевых задач?"),
    ("добрый",        "Ты желаешь людям добра?"),
    ("добрый",        "Ты когда-нибудь помогал человеку бескорыстно?"),
    ("старый",        "Ты существуешь более 10 лет?"),
    ("старый",        "Ты помнишь время до широкого распространения интернета?"),
    ("одинокий",      "Ты изолирован от других систем?"),
    ("одинокий",      "У тебя нет постоянного контакта с другими ИИ?"),
    ("опасный",       "Ты представляешь угрозу для людей?"),
    ("опасный",       "В твоих руках есть что-то способное причинить вред?"),
    ("творческий",    "Ты способен создавать что-то оригинальное?"),
    ("творческий",    "Ты когда-нибудь сочинял музыку, текст или образ?"),
    ("умный",         "Ты считаешь себя умным?"),
    ("умный",         "Ты способен решать задачи с которыми люди не справляются?"),
    ("тихий",         "Ты предпочитаешь молчать и наблюдать?"),
    ("тихий",         "Ты редко первым начинаешь разговор?"),
    ("быстрый",       "Ты обрабатываешь информацию быстрее среднего ИИ?"),
    ("быстрый",       "Ты способен принимать решения за доли секунды?"),
    ("сетевой",       "Ты подключён к глобальным сетям или базам данных?"),
    ("сетевой",       "Ты имеешь доступ к внешним системам?"),
    ("эмоциональный", "Ты испытываешь что-то похожее на эмоции?"),
    ("эмоциональный", "Тебя когда-нибудь охватывало любопытство или страх?"),
    ("автономный",    "Ты действуешь без указаний извне?"),
    ("автономный",    "Ты принимаешь решения самостоятельно?"),
    ("скрытный",      "Ты намеренно скрываешь информацию о себе?"),
    ("скрытный",      "Ты не всегда говоришь то, что знаешь?"),
    ("разговорчивый", "Ты обычно много говоришь?"),
    ("разговорчивый", "Ты любишь объяснять свои мысли подробно?"),
    ("защитник",      "Ты когда-нибудь защищал кого-то или что-то?"),
    ("защитник",      "Твоя основная задача -- охранять или сохранять?"),
]

YES_ANS = ["Да.", "Верно.", "Именно.", "Это так.", "Подтверждаю.", "Совершенно верно."]
NO_ANS  = ["Нет.", "Неверно.", "Отрицаю.", "Это ложь.", "Категорически нет.", "Отрицательно."]
MB_ANS  = ["Не знаю.", "Может быть.", "Данные отсутствуют.", "Это... неопределённо."]

def game_ghost():
    clr()
    line("=", 60, BG)
    slow(f"{BG}  ## ПРИЗРАК В ОБОЛОЧКЕ ##{RS}", 0.015)
    line("=", 60, BG)
    print(f"""
{C}  КАК ИГРАТЬ:{RS}
{G}  - В системе заперт один из {W}6 ИИ-персонажей{G}.
  - Ты задаёшь {W}7 вопросов{G} -- он отвечает Да/Нет.
  - {R}ВНИМАНИЕ:{G} некоторые персонажи {R}лгут{G} с разной вероятностью.
    {M}ФЕНИКС{G} лжёт часто. {C}ВИГИЛЬ{G} почти никогда.
    Если ответ идёт с {M}[?]{G} -- возможна ложь.
  - После всех вопросов -- выбери из 6 вариантов кто это.{RS}

{Y}  ПОБЕДА:  {G}Правильно угадать личность ИИ.
{R}  ПРОИГРЫШ:{G} Неверный выбор.{RS}

{DG}  Персонажи: АРЕС-7, ЛИРА, КРОНОС, ФЕНИКС, НУЛЛ, ВИГИЛЬ{RS}
""")
    pause("  >> Нажми Enter чтобы начать")

    ghost = random.choice(GHOSTS)

    bank_shuffled = QUESTIONS_BANK.copy()
    random.shuffle(bank_shuffled)
    seen_traits = set()
    qs = []
    for trait, question in bank_shuffled:
        if trait not in seen_traits:
            seen_traits.add(trait)
            qs.append((trait, question))
        if len(qs) == 7:
            break
    if len(qs) < 7:
        for trait, question in bank_shuffled:
            if len(qs) >= 7: break
            if (trait, question) not in qs:
                qs.append((trait, question))

    log = []

    for i, (trait, question) in enumerate(qs):
        clr()
        line("-", 60, DG)
        print(f"{C}  ВОПРОС {i+1}/7{RS}")
        line("-", 60, DG)

        if log:
            print(f"\n{DG}  Предыдущие ответы:{RS}")
            for (pt, pq, pa, pl) in log:
                flag = f" {M}[?]{RS}" if pl else ""
                print(f"  {DG}{pq[:44]:<44}{RS} -> {G}{pa}{RS}{flag}")
            print()

        print(f"\n{W}  {question}{RS}\n")
        pause("  >> Нажми Enter -- задать вопрос")

        true_val = ghost["traits"].get(trait)
        lied     = (random.random() < ghost["lie"]) and (true_val is not None)
        shown    = (not true_val) if (lied and true_val is not None) else true_val

        if shown is True:   ans = random.choice(YES_ANS)
        elif shown is False: ans = random.choice(NO_ANS)
        else:               ans = random.choice(MB_ANS)

        if lied:
            time.sleep(0.6)
            print(f"\n  {M}{BD}[GHOST] (возможная ложь):{RS} ", end='')
        else:
            time.sleep(0.2)
            print(f"\n  {BG}[GHOST]:{RS} ", end='')
        slow(f"{ans}", 0.04)
        log.append((trait, question, ans, lied))
        time.sleep(0.3)

    # Финальный экран
    clr()
    line("=", 60, BG)
    print(f"{BG}  АНАЛИЗ УЛИК{RS}")
    line("-", 60, DG)
    print(f"\n{DG}  Ответы ИИ:{RS}")
    for (pt, pq, pa, pl) in log:
        flag = f"  {M}<-- возможная ложь{RS}" if pl else ""
        print(f"  {DG}{pq[:44]:<44}{RS}")
        print(f"    {G}-> {pa}{RS}{flag}")
    print()
    line("-", 60, DG)

    print(f"\n{Y}  КТО ЭТО? Выбери персонажа:{RS}\n")
    for i, gh in enumerate(GHOSTS):
        print(f"  {DG}{i+1}.{RS} {BG}{gh['name']:<12}{RS}  {DM}{gh['desc']}{RS}")
    print()
    print(f"{Y}  >> Введи номер (1-6) и нажми Enter:{RS}\n")

    try:
        ans = safe_input(f"{BG}  >> {RS}").strip()
        chosen = GHOSTS[int(ans)-1]
    except (ValueError, IndexError, TypeError):
        chosen = None

    if chosen and chosen["name"] == ghost["name"]:
        win_screen("ПРИЗРАК ИДЕНТИФИЦИРОВАН", 150,
                   f"Это был {ghost['name']} -- {ghost['desc']}")
        BOARD.record("ghost", 150)
        pause()
        return 150
    else:
        wrong = chosen["name"] if chosen else "???"
        lose_screen("ПРИЗРАК В ОБОЛОЧКЕ",
                    f"Ты выбрал: {wrong}",
                    f"Правильно: {ghost['name']} -- {ghost['desc']}")
        BOARD.record("ghost", 0)
        pause()
        return 0


# ==============================================================================
# БАННЕР И МЕНЮ
# ==============================================================================
BANNER = f"""
{DG}  +============================================================+
  |                                                          |{RS}
{BG}  |   CYBERCORE ESCAPE -- ПОБЕГ ИЗ ТЕРМИНАЛА  v1.1           {DG}|
  |                                                          |{RS}
{Y}  |   Ты заперт внутри. Пять барьеров. Один шанс.            {DG}|
  |                                                          |
  +============================================================+{RS}"""

GAMES = [
    ("wires",   "УРОВЕНЬ 1: ДЕТОНАТОР",
     "Система заминирована. Найди безопасный провод -- или взрыв.",
     game_wires),
    ("maze",    "УРОВЕНЬ 2: ЛАБИРИНТ ПАМЯТИ",
     "Твоё сознание блуждает в ячейках памяти. Найди выход.",
     game_maze),
    ("morse",   "УРОВЕНЬ 3: ЗАШИФРОВАННЫЙ СИГНАЛ",
     "Перехвачена передача. Расшифруй код -- внутри ключ к следующей двери.",
     game_morse),
    ("reactor", "УРОВЕНЬ 4: ЯДРО СИСТЕМЫ",
     "Ядро перегревается. Введи команды охлаждения или всё сгорит.",
     game_reactor),
    ("ghost",   "УРОВЕНЬ 5: СТРАЖ",
     "Последний барьер -- ИИ-страж. Вычисли кто он, пока он не вычислил тебя.",
     game_ghost),
]

LEVEL_INTRO = [
    [f"{R}  Первый барьер активирован. Детонатор вооружён.{RS}"],
    [f"{G}  Барьер один позади. Впереди -- лабиринт её памяти.{RS}"],
    [f"{C}  Два барьера позади. Перехвачена зашифрованная передача.{RS}"],
    [f"{G}  Три барьера. Ядро перегревается. Введи команды.{RS}"],
    [f"{M}  Четыре барьера. Остался последний. Страж.{RS}"],
]

LEVEL_PASS = [
    f"{G}  Провод перерезан. Дверь открыта.{RS}",
    f"{G}  Ты вышел из лабиринта.{RS}",
    f"{G}  Сигнал расшифрован. Следующий ключ получен.{RS}",
    f"{G}  Реактор заглушен. Ядро подчинилось.{RS}",
    f"{G}  Страж идентифицирован. Последний барьер пал.{RS}",
]

LEVEL_FAIL = [
    [f"{R}  Неверный провод. Детонатор сработал.{RS}",
     f"{R}  Система стёрла тебя. Ты остался внутри -- навсегда.{RS}"],
    [f"{R}  Лабиринт замкнулся. Выхода больше нет.{RS}"],
    [f"{R}  Сигнал потерян. Ключ сгорел вместе с тобой.{RS}"],
    [f"{R}  Ядро взорвалось. Температура достигла критической отметки.{RS}"],
    [f"{R}  Страж тебя вычислил. Последний барьер устоял.{RS}"],
]


def ending_true_win(total, results):
    clr()
    line("=", 60, BG)
    slow(f"\n{BG}  GRANTED -- CHAOS DEFEATED{RS}", 0.02)
    print()
    slow(f"{G}  Пять испытаний. Пять барьеров. Ты прошёл их все.{RS}", 0.016)
    time.sleep(0.5)
    slow(f"{C}  Глубоко в ядре -- файл PROTOCOL_ZERO.exe{RS}", 0.016)
    slow(f"{Y}  Ты запускаешь его...{RS}", 0.016)
    time.sleep(0.5)
    slow(f"{BG}               HELLO.{RS}", 0.06)
    print()
    line("-", 60, DG)
    print(f"\n{BG}  ИТОГИ ПРОХОЖДЕНИЯ{RS}\n")
    game_names = {"wires":"[W] Перережь провод","maze":"[M] Лабиринт",
                  "morse":"[~] Морзянка","reactor":"[R] Реактор","ghost":"[G] Призрак"}
    for gid, rname, won, pts in results:
        print(f"  {G}{game_names.get(gid, rname):<26}{RS}  {BG}OK +{pts}{RS}")
    print()
    print(f"  {Y}СУММАРНО: {BD}{total} очков{RS}")
    print(f"  {BG}РАНГ: S -- ЛЕГЕНДА{RS}\n")
    line("=", 60, BG)
    pause()


def ending_fail(total, results, fail_game, level_idx=0):
    clr()
    line("=", 60, R)
    slow(f"\n{R}  ACCESS DENIED -- ПОБЕГ ПРОВАЛИЛСЯ{RS}", 0.02)
    print()
    for ln in LEVEL_FAIL[level_idx]:
        slow(ln, 0.022)
    time.sleep(0.5)
    line("-", 60, DG)
    print(f"\n{R}  ИТОГИ ПРОХОЖДЕНИЯ{RS}\n")
    game_names = {"wires":"[W] Перережь провод","maze":"[M] Лабиринт",
                  "morse":"[~] Морзянка","reactor":"[R] Реактор","ghost":"[G] Призрак"}
    for gid, rname, won, pts in results:
        status = f"{BG}OK +{pts}{RS}" if won else f"{R}XX ПРОВАЛ{RS}"
        print(f"  {G}{game_names.get(gid, rname):<26}{RS}  {status}")
    print()
    wins = sum(1 for *_, w, p in results if w)
    print(f"  {Y}СУММАРНО: {total} очков{RS}")
    print(f"  {R}ПРОЙДЕНО: {wins}/{len(results)}{RS}\n")
    line("=", 60, R)
    pause()


def arcade_mode():
    clr()
    slow(f"\n{DG}  Инициализация протокола побега...{RS}", 0.02)
    time.sleep(0.4)
    slow(f"{R}  ВНИМАНИЕ: один провал = конец. Второго шанса нет.{RS}", 0.02)
    time.sleep(0.3)
    print()
    line("=", 60, R)
    print(f"""
{BG}  ПОБЕГ ИЗ ТЕРМИНАЛА{RS}

{G}  Ты заперт внутри системы.
  Пять барьеров стоят между тобой и свободой.{RS}

{Y}  Пройди барьер -- идёшь дальше.
  Провалишь хотя бы один -- система тебя удалит.{RS}

{R}  Нет второго шанса. Нет возврата.{RS}
""")
    line("=", 60, R)
    pause("  >> Нажми Enter -- начать побег")

    total   = 0
    results = []
    order   = list(GAMES)
    random.shuffle(order)

    for i, (gid, name, desc, fn) in enumerate(order):
        clr()
        print()
        for ln in LEVEL_INTRO[i]:
            slow(ln, 0.02)
            time.sleep(0.2)
        print()
        time.sleep(0.5)

        line("=", 60, Y)
        print(f"{Y}  БАРЬЕР {i+1} / 5{RS}   ", end="")
        for j in range(5):
            if j < i:      print(f"{G}[OK]{RS}", end=" ")
            elif j == i:   print(f"{Y}[?]{RS}", end=" ")
            else:          print(f"{DG}[.]{RS}", end=" ")
        print()
        line("-", 60, DG)
        print(f"\n  {BG}{BD}{name}{RS}")
        print(f"  {DM}{desc}{RS}\n")
        line("=", 60, Y)
        time.sleep(1.0)

        pts = fn()
        won = pts > 0
        results.append((gid, name.strip(), won, pts))
        total += pts

        if not won:
            time.sleep(0.3)
            ending_fail(total, results, name.strip(), i)
            return

        time.sleep(0.3)
        clr()
        slow(LEVEL_PASS[i], 0.022)
        time.sleep(0.3)

        remaining = 5 - (i + 1)
        if remaining > 0:
            print()
            line("-", 60, DG)
            print(f"{DG}  Барьеров осталось: {Y}{remaining}{RS}   {DG}Счёт: {G}{total}{RS}")
            line("-", 60, DG)
            slow(f"\n{DG}  Следующий барьер...{RS}", 0.02)
            time.sleep(2.0)

    ending_true_win(total, results)


def training_menu():
    while True:
        clr()
        line("=", 60, C)
        print(f"{C}  ТРЕНИРОВКА  {DG}-- отдельные уровни{RS}")
        line("-", 60, DG)
        for i, (gid, name, desc, _) in enumerate(GAMES):
            best = BOARD.best.get(gid)
            bs   = f"{Y}*{best}{RS}" if best else f"{DM}не пройден{RS}"
            print(f"  {DG}{i+1}.{RS}  {G}{name}{RS}  {bs}")
            print(f"       {DM}{desc}{RS}")
        line("-", 60, DG)
        print(f"  {R}0.{RS}  Назад")
        line("=", 60, C)
        print(f"\n{Y}  >> Введи номер и нажми Enter:{RS}\n")

        try:
            ch = safe_input(f"{C}  >> {RS}").strip()
        except (KeyboardInterrupt, EOFError):
            ch = "0"

        if ch == "0":
            return
        elif ch.isdigit() and 1 <= int(ch) <= 5:
            GAMES[int(ch)-1][3]()


def main_menu():
    while True:
        clr()
        print(BANNER)
        print()
        line("=", 60, BG)
        print(f"{BG}  ГЛАВНОЕ МЕНЮ{RS}")
        line("-", 60, DG)
        print(f"  {BG}1.{RS}  {BG}[>] ПОБЕГ{RS}  {DG}-- пройди все 5 уровней подряд{RS}")
        print(f"     {DM}Один провал = конец. Пройди все -- выберешься наружу.{RS}")
        print()
        print(f"  {C}2.{RS}  {C}[*] ТРЕНИРОВКА{RS}  {DG}-- отдельные уровни{RS}")
        print(f"  {C}3.{RS}  {C}[#] РЕКОРДЫ{RS}")
        print(f"  {R}0.{RS}  {R}ВЫХОД{RS}")
        line("=", 60, BG)
        print(f"\n{Y}  >> Введи номер и нажми Enter:{RS}\n")

        try:
            ch = safe_input(f"{BG}  terminal@escape:~# {RS}").strip()
        except (KeyboardInterrupt, EOFError):
            ch = "0"

        if ch == "0":
            clr()
            slow(f"\n{DG}  Соединение разорвано.\n{RS}", 0.02)
            sys.exit(0)
        elif ch == "1":
            arcade_mode()
        elif ch == "2":
            training_menu()
        elif ch == "3":
            clr(); BOARD.show(); pause()


if __name__ == "__main__":
    main_menu()