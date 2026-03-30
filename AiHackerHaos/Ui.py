"""
ui.py -- ANSI-цвета, утилиты вывода, ASCII-баннер
"""
import time

# --- ANSI-цвета ---------------------------------------------------------------
GREEN        = "\033[92m"
BRIGHT_GREEN = "\033[1;92m"
DIM_GREEN    = "\033[2;32m"
RED          = "\033[91m"
YELLOW       = "\033[93m"
CYAN         = "\033[96m"
WHITE        = "\033[97m"
MAGENTA      = "\033[95m"
BLUE         = "\033[94m"
DIM          = "\033[2m"
BOLD         = "\033[1m"
BLINK        = "\033[5m"
RESET        = "\033[0m"

def g(t):    return f"{GREEN}{t}{RESET}"
def bg(t):   return f"{BRIGHT_GREEN}{t}{RESET}"
def r(t):    return f"{RED}{t}{RESET}"
def y(t):    return f"{YELLOW}{t}{RESET}"
def c(t):    return f"{CYAN}{t}{RESET}"
def m(t):    return f"{MAGENTA}{t}{RESET}"
def dim(t):  return f"{DIM_GREEN}{t}{RESET}"

def slow_print(text, delay=0.018):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def type_print(text, delay=0.010):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def scan_line(char="-", length=60, color=None):
    color = color or DIM_GREEN
    print(f"{color}{char * length}{RESET}")

# --- Баннер -------------------------------------------------------------------
BANNER = f"""
{BRIGHT_GREEN}
  @@@@@@  @@@  @@@  @@@@@@@  @@@@@@@@  @@@@@@@   @@@@@@@   @@@@@@   @@@@@@@   @@@@@@@@
 @@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@
 @@!  @@@  @@!  @@!  @@!  @@@  @@!       @@!  @@@  !@@       @@!  @@@  @@!  @@@  @@!
 !@!  @!@  !@!  !@!  !@!  @!@  !@!       !@!  @!@  !@!       !@!  @!@  !@!  @!@  !@!
 @!@!@!@!  @!!  !!@  @!@!!@!   @!!!:!    @!@!!@!   !@!       @!@  !@!  @!@!!@!   @!!!:!
 !!!@!!!!  !@@  !!!  !!@!@!    !!!!!:    !!@!@!    !!!       !@!  !!!  !!@!@!    !!!!!:
 !!:  !!!  !!:       !!: :!!   !!:       !!: :!!   :!!       !!:  !!!  !!: :!!   !!:
 :!:  !:!  :!:       :!:  !:!  :!:       :!:  !:!  :!:       :!:  !:!  :!:  !:!  :!:
 ::   :::   ::       ::   :::   :: ::::  ::   :::   ::: :::  ::::: ::  ::   :::   :: ::::
  :   : :   :         :   : :  : :: ::    :   : :   :: :: :   : :  :    :   : :  : :: ::
{RESET}{RED}
  @@@@@@  @@@  @@@ @@@@@@   @@@@@@   @@@@@@      @@@@@@@@  @@@@@@@  @@@  @@@@@@@
 !@@     @@!  @@@ @@!  @@@ @@!  @@@ !@@         @@!       @@!  @@@ @@! !@@
 !@!     @!@!@!@! @!@!@!@! @!@  !@! !@! @!@!@   @!!!:!    @!@  !@@ !!@  !@@!!
 :!!     !!:  !!! !!:  !!! !!:  !!!  !:!   !!:  !!:       !!:  !!!  !!      !:!
  :: :: :  :   :   :   : :  :   : :   :!: :::   : :: :::  :: :  :    :  ::.: :
{RESET}
{DIM_GREEN}              [ PROTOCOL v2.4.1 -- ХАОС-РЕЖИМ АКТИВЕН ]
              [ ВНИМАНИЕ: СИСТЕМА НЕСТАБИЛЬНА. ФИЛЬТРУЙ ШУМ. ]
{RESET}"""