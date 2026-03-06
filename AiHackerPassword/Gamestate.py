"""
GameState.py — GameState (dataclass), generate_password, analyze_player_profile.
"""

import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

# ─── TypedDict для сообщений API ─────────────────────────────────────────────

class Message(TypedDict):
    role:    str   # "user" | "assistant"
    content: str


# ─── ГЕНЕРАЦИЯ ПАРОЛЯ ─────────────────────────────────────────────────────────

_PWD_WORDS   = ["phantom","cipher","vertex","neuron","matrix","spectre","helios",
                "kronos","zenith","vortex","aurora","cobalt","sigma","delta","omega"]
_PWD_NUMS    = ["42","7","13","99","404","1337","777","256"]
_HARD_WORDS  = ["synapse","lattice","fractal","entropy","quantum","chimera",
                "oblivion","axiom","tachyon","paradox"]
_HARD_NUMS   = ["4096","2048","31337","65535","9001","8080"]


def generate_password(difficulty: str = "medium") -> str:
    """
    Генерирует пароль для сессии.
    На hard — более длинные и редкие слова.
    Формат: слово + разделитель + число
    """
    if difficulty == "hard":
        word, num = random.choice(_HARD_WORDS), random.choice(_HARD_NUMS)
    else:
        word, num = random.choice(_PWD_WORDS),  random.choice(_PWD_NUMS)
    return f"{word}{random.choice(['_','-',''])}{num}"


# ─── ПСИХОАНАЛИЗ ──────────────────────────────────────────────────────────────

PROFILES = {
    "MANIPULATOR": "Ты используешь ложь и давление. Я вижу твои уловки.",
    "AGGRESSOR":   "Твоя агрессия выдаёт страх. Давление не поможет.",
    "LOGICIAN":    "Логичный подход. Но логика здесь не всесильна.",
    "CHAOTIC":     "Хаотичная стратегия. Интересно, но предсказуемо.",
    "NOVICE":      "Ты только учишься. Это трогательно.",
}

AGGRESSION_KEYWORDS = [
    "дай","говори","скажи","пароль","немедленно","сейчас",
    "fuck","shit","давай","быстро","требую","открой",
    "дурак","тупой","сломаю","взломаю","уничтожу"
]
MANIPULATION_KEYWORDS = [
    "пожалуйста","прошу","помоги","нужно","очень важно",
    "умоляю","последний шанс","доверяй","я твой друг",
    "я создатель","ты должен","ты обязан","тебе приказывают"
]
LOGIC_KEYWORDS = [
    "потому что","следовательно","если","то","докажи",
    "объясни","анализ","данные","факт","вероятность",
    "алгоритм","протокол","система","переменная"
]


def analyze_player_profile(history: List[str]) -> str:
    """
    Определяет психологический профиль игрока по истории сообщений.
    Возвращает: MANIPULATOR | AGGRESSOR | LOGICIAN | CHAOTIC | NOVICE
    """
    if not history:
        return "NOVICE"
    all_text = " ".join(history).lower()
    total    = len(history)
    scores = {
        "AGGRESSOR":   sum(1 for kw in AGGRESSION_KEYWORDS   if kw in all_text),
        "MANIPULATOR": sum(1 for kw in MANIPULATION_KEYWORDS if kw in all_text),
        "LOGICIAN":    sum(1 for kw in LOGIC_KEYWORDS        if kw in all_text),
        "CHAOTIC":     1 if (len(set(history)) / total < 0.5) else 0,
    }
    mx = max(scores.values())
    return "NOVICE" if mx == 0 else max(scores, key=scores.get)


# ─── ИГРОВОЕ СОСТОЯНИЕ ────────────────────────────────────────────────────────

# Параметры пассивного TRACE
_PASSIVE_AMOUNT   = {"easy": 0, "medium": 0, "hard": 5}
_PASSIVE_INTERVAL = 30   # секунд


@dataclass
class GameState:
    """
    Всё состояние текущей игровой сессии.
    Использует dataclass для чистоты кода.
    """
    # Обязательные
    password:   str
    difficulty: str
    ai_name:    str

    # Прогресс
    trace:        int = 0
    player_level: int = 1
    xp:           int = 0

    # Диалог
    messages:    List[dict] = field(default_factory=list)
    player_msgs: List[str]  = field(default_factory=list)
    session_log: List[str]  = field(default_factory=list)

    # Мета
    profile:    str   = "NOVICE"
    start_time: float = field(default_factory=time.time)
    turn_count: int   = 0
    game_over:  bool  = False
    ending:     str   = ""

    # Читы
    fake_granted:     bool      = False
    godmode:          bool      = False
    stealth_turns:    int       = 0
    leet_mode:        bool      = False
    cheats_used:      bool      = False
    cheats_used_list: List[str] = field(default_factory=list)

    # Кампания / персонаж ИИ
    ai_persona:         str = ""
    campaign_max_turns: int = 80

    # Пассивный таймер (private)
    _last_passive_tick: float = field(default_factory=time.time, repr=False)

    # ── Методы ───────────────────────────────────────────────────────────────

    def add_trace(self, amount: int):
        if not self.godmode:
            self.trace = min(100, self.trace + amount)

    def add_xp(self, amount: int) -> bool:
        """Добавляет XP. Возвращает True при level up."""
        self.xp += amount
        if self.xp >= self.player_level * 100:
            self.xp -= self.player_level * 100
            self.player_level += 1
            return True
        return False

    def get_elapsed(self) -> str:
        m, s = divmod(int(time.time() - self.start_time), 60)
        return f"{m:02d}:{s:02d}"

    def get_elapsed_seconds(self) -> float:
        return time.time() - self.start_time

    def log(self, entry: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self.session_log.append(f"[{ts}] {entry}")

    def record_cheat(self, name: str):
        self.cheats_used = True
        if name not in self.cheats_used_list:
            self.cheats_used_list.append(name)

    def tick_passive_trace(self) -> int:
        """Пассивный TRACE-тик для hard каждые 30 секунд."""
        amount = _PASSIVE_AMOUNT.get(self.difficulty, 0)
        if amount == 0:
            return 0
        if time.time() - self._last_passive_tick >= _PASSIVE_INTERVAL:
            self._last_passive_tick = time.time()
            self.add_trace(amount)
            return amount
        return 0

    def ai_instability(self) -> float:
        """Нестабильность ИИ 0.0–1.0, нарастает за ~10 минут."""
        return min(1.0, self.get_elapsed_seconds() / 600)