import sys, time, random
from Utils import clr, slow, line, pause, G, BG, DG, R, Y, C, W, M, DM, BD, RS
from Scoreboard import BOARD
from GamesWiresMaze  import game_wires, game_maze
from GamesMorseReactor import game_morse, game_reactor
from GameGhost        import game_ghost

# ==============================================================================
# РЕГИСТР ИГР
# ==============================================================================
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

BANNER = f"""
{DG}  +============================================================+
  |                                                          |{RS}
{BG}  |   CYBERCORE ESCAPE -- ПОБЕГ ИЗ ТЕРМИНАЛА  v1.1           {DG}|
  |                                                          |{RS}
{Y}  |   Ты заперт внутри. Пять барьеров. Один шанс.            {DG}|
  |                                                          |
  +============================================================+{RS}"""


# ==============================================================================
# КОНЦОВКИ
# ==============================================================================
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


# ==============================================================================
# РЕЖИМЫ
# ==============================================================================
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
    from Utils import safe_input
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
    from Utils import safe_input
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