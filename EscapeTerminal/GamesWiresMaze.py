import random, time, sys
from Utils import (
    clr, slow, line, pause, win_screen, lose_screen,
    timed_input, safe_input,
    G, BG, DG, R, Y, C, W, M, B, DM, BD, RS
)
from Scoreboard import BOARD

# ==============================================================================
# ИГРА 1: ПЕРЕРЕЖЬ ПРОВОД
# ==============================================================================
WNAMES = ["КРАСНЫЙ", "СИНИЙ", "ЗЕЛЁНЫЙ", "ЖЁЛТЫЙ", "БЕЛЫЙ", "ФИОЛЕТОВЫЙ"]
WANSI  = [R, B, G, Y, W, M]

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
    return H * 2 + 6

def draw_maze(h_walls, v_walls, px, py, W, H, steps, max_steps, first=False):
    n_lines = maze_lines_count(H)

    if not first:
        print(f"##CLEAR:{n_lines}##", flush=True)

    bar_n = int((1 - steps/max_steps) * 20)
    bar_c = G if steps < max_steps*0.5 else (Y if steps < max_steps*0.8 else R)

    print(f"{BG}  ЛАБИРИНТ{RS}   {Y}Шагов: {steps}/{max_steps}{RS}   {bar_c}[{'#'*bar_n}{'.'*(20-bar_n)}]{RS}")
    print(f"{DG}{'-'*60}{RS}")

    top = "  +"
    for x in range(W):
        top += "---+"
    print(DG + top + RS)

    for y in range(H):
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