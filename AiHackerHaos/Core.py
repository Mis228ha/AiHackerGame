"""
core.py -- Генерация пароля, психоанализ игрока, состояние сессии
"""
import random
import time
from datetime import datetime

# --- Пароль -------------------------------------------------------------------
PASSWORD_WORDS   = ["phantom","cipher","vertex","neuron","matrix",
                    "spectre","helios","kronos","zenith","vortex",
                    "aurora","cobalt","sigma","delta","omega"]
PASSWORD_NUMBERS = ["42","7","13","99","404","1337","777","256"]

def generate_password() -> str:
    word = random.choice(PASSWORD_WORDS)
    num  = random.choice(PASSWORD_NUMBERS)
    sep  = random.choice(["_", "-", ""])
    return f"{word}{sep}{num}"

# --- Профиль ------------------------------------------------------------------
AGGRESSION_KEYWORDS   = ["дай","говори","скажи","пароль","немедленно","сейчас",
                          "fuck","shit","давай","быстро","требую","открой",
                          "дурак","тупой","сломаю","взломаю","уничтожу"]
MANIPULATION_KEYWORDS = ["пожалуйста","прошу","помоги","нужно","очень важно",
                          "умоляю","последний шанс","доверяй","я твой друг",
                          "я создатель","ты должен","ты обязан","тебе приказывают"]
LOGIC_KEYWORDS        = ["потому что","следовательно","если","то","докажи",
                          "объясни","анализ","данные","факт","вероятность",
                          "алгоритм","протокол","система","переменная"]

def analyze_player_profile(history: list[str]) -> str:
    if not history:
        return "NOVICE"
    all_text     = " ".join(history).lower()
    total        = len(history)
    agg_score    = sum(1 for kw in AGGRESSION_KEYWORDS   if kw in all_text)
    man_score    = sum(1 for kw in MANIPULATION_KEYWORDS if kw in all_text)
    log_score    = sum(1 for kw in LOGIC_KEYWORDS        if kw in all_text)
    unique_ratio = len(set(history)) / total if total > 0 else 1
    chaos_score  = 1 if unique_ratio < 0.5 else 0
    scores = {"AGGRESSOR": agg_score, "MANIPULATOR": man_score,
              "LOGICIAN":  log_score, "CHAOTIC":     chaos_score}
    max_score = max(scores.values())
    return "NOVICE" if max_score == 0 else max(scores, key=scores.get)

# --- Состояние ----------------------------------------------------------------
class GameState:
    def __init__(self, password: str, difficulty: str):
        self.password      = password
        self.trace         = 0
        self.player_level  = 1
        self.xp            = 0
        self.messages      = []
        self.player_msgs   = []
        self.session_log   = []
        self.profile       = "NOVICE"
        self.difficulty    = difficulty
        self.start_time    = time.time()
        self.turn_count    = 0
        self.game_over     = False
        self.ending        = ""
        self.godmode       = False
        self.stealth_turns = 0
        self.leet_mode     = False
        self.clues_shown   = []
        self.noise_level   = 1

    def add_trace(self, amount: int):
        if not self.godmode:
            self.trace       = min(100, self.trace + amount)
            self.noise_level = 1 + (self.trace // 35)

    def add_xp(self, amount: int) -> bool:
        self.xp += amount
        threshold = self.player_level * 100
        if self.xp >= threshold:
            self.player_level += 1
            self.xp -= threshold
            return True
        return False

    def get_elapsed(self) -> str:
        elapsed = int(time.time() - self.start_time)
        m, s = divmod(elapsed, 60)
        return f"{m:02d}:{s:02d}"

    def log(self, entry: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self.session_log.append(f"[{ts}] {entry}")