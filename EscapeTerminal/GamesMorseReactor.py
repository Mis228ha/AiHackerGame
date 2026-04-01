import random, time
from Utils import (
    clr, slow, line, pause, win_screen, lose_screen,
    timed_input, safe_input,
    G, BG, DG, R, Y, C, W, M, DM, BD, RS
)
from Scoreboard import BOARD

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