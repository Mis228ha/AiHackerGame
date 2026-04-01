from Utils import BG, G, Y, DM, DG, R, RS, BD

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