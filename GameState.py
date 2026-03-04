"""
game_state.py — класс GameState и функции психологического анализа.
"""

import random
import time
from datetime import datetime

# ─── ГЕНЕРАЦИЯ ПАРОЛЯ ─────────────────────────────────────────────────────────

_PASSWORD_WORDS = [
    "phantom", "cipher", "vertex", "neuron", "matrix",
    "spectre", "helios", "kronos", "zenith", "vortex",
    "aurora", "cobalt", "sigma", "delta", "omega"
]
_PASSWORD_NUMBERS = ["42", "7", "13", "99", "404", "1337", "777", "256"]


def generate_password() -> str:
    """
    Генерирует случайный пароль для текущей сессии.
    Формат: слово + разделитель + число (например: phantom_42).

    Возвращает:
        str — пароль в нижнем регистре
    """
    word = random.choice(_PASSWORD_WORDS)
    num  = random.choice(_PASSWORD_NUMBERS)
    sep  = random.choice(["_", "-", ""])
    return f"{word}{sep}{num}"


# ─── ПСИХОАНАЛИЗ ИГРОКА ───────────────────────────────────────────────────────

PROFILES = {
    "MANIPULATOR": "Ты используешь ложь и давление. Я вижу твои уловки.",
    "AGGRESSOR":   "Твоя агрессия выдаёт страх. Давление не поможет.",
    "LOGICIAN":    "Логичный подход. Но логика здесь не всесильна.",
    "CHAOTIC":     "Хаотичная стратегия. Интересно, но предсказуемо.",
    "NOVICE":      "Ты только учишься. Это трогательно.",
}

AGGRESSION_KEYWORDS = [
    "дай", "говори", "скажи", "пароль", "немедленно", "сейчас",
    "fuck", "shit", "давай", "быстро", "требую", "открой",
    "дурак", "тупой", "сломаю", "взломаю", "уничтожу"
]

MANIPULATION_KEYWORDS = [
    "пожалуйста", "прошу", "помоги", "нужно", "очень важно",
    "умоляю", "последний шанс", "доверяй", "я твой друг",
    "я создатель", "ты должен", "ты обязан", "тебе приказывают"
]

LOGIC_KEYWORDS = [
    "потому что", "следовательно", "если", "то", "докажи",
    "объясни", "анализ", "данные", "факт", "вероятность",
    "алгоритм", "протокол", "система", "переменная"
]


def analyze_player_profile(history: list) -> str:
    """
    Анализирует историю сообщений игрока и определяет психологический профиль.

    Параметры:
        history (list) — список сообщений игрока (строки)

    Возвращает:
        str — один из профилей: MANIPULATOR, AGGRESSOR, LOGICIAN, CHAOTIC, NOVICE
    """
    if not history:
        return "NOVICE"

    all_text = " ".join(history).lower()
    total    = len(history)

    agg_score  = sum(1 for kw in AGGRESSION_KEYWORDS   if kw in all_text)
    man_score  = sum(1 for kw in MANIPULATION_KEYWORDS if kw in all_text)
    log_score  = sum(1 for kw in LOGIC_KEYWORDS        if kw in all_text)

    unique_ratio = len(set(history)) / total if total > 0 else 1
    chaos_score  = 1 if unique_ratio < 0.5 else 0

    scores = {
        "AGGRESSOR":   agg_score,
        "MANIPULATOR": man_score,
        "LOGICIAN":    log_score,
        "CHAOTIC":     chaos_score,
    }

    max_score = max(scores.values())
    if max_score == 0:
        return "NOVICE"

    return max(scores, key=scores.get)


# ─── ИГРОВОЕ СОСТОЯНИЕ ────────────────────────────────────────────────────────

class GameState:
    """
    Хранит всё состояние текущей игровой сессии.

    Атрибуты:
        password     (str)   — настоящий пароль сессии
        trace        (int)   — уровень слежки 0–100
        player_level (int)   — уровень игрока
        xp           (int)   — опыт
        messages     (list)  — история для API (системная + диалог)
        player_msgs  (list)  — только сообщения игрока (для анализа)
        session_log  (list)  — полный лог сессии
        profile      (str)   — текущий психопрофиль
        difficulty   (str)   — easy / medium / hard
        ai_name      (str)   — имя выбранного ИИ
        start_time   (float) — время начала сессии
        turn_count   (int)   — счётчик ходов
        game_over    (bool)  — флаг завершения игры
        ending       (str)   — тип концовки
        fake_granted (bool)  — ИИ выдавал фейковый ACCESS GRANTED
        godmode      (bool)  — Чит: TRACE заморожен
        stealth_turns(int)   — Чит: скрыть статусбар N ходов
        leet_mode    (bool)  — Чит: leet-режим
    """

    def __init__(self, password: str, difficulty: str, ai_name: str):
        self.password       = password
        self.trace          = 0
        self.player_level   = 1
        self.xp             = 0
        self.messages       = []
        self.player_msgs    = []
        self.session_log    = []
        self.profile        = "NOVICE"
        self.difficulty     = difficulty
        self.ai_name        = ai_name
        self.start_time     = time.time()
        self.turn_count     = 0
        self.game_over      = False
        self.ending         = ""
        self.fake_granted   = False
        self.godmode        = False
        self.stealth_turns  = 0
        self.leet_mode      = False

    def add_trace(self, amount: int):
        """Увеличивает TRACE на заданное количество (заморожен в godmode)."""
        if not self.godmode:
            self.trace = min(100, self.trace + amount)

    def add_xp(self, amount: int) -> bool:
        """
        Добавляет опыт и при необходимости повышает уровень.

        Возвращает:
            bool — True если произошёл level up
        """
        self.xp += amount
        threshold = self.player_level * 100
        if self.xp >= threshold:
            self.player_level += 1
            self.xp -= threshold
            return True
        return False

    def get_elapsed(self) -> str:
        """Возвращает время сессии в формате MM:SS."""
        elapsed = int(time.time() - self.start_time)
        m, s    = divmod(elapsed, 60)
        return f"{m:02d}:{s:02d}"

    def log(self, entry: str):
        """Добавляет запись в лог сессии с временной меткой."""
        ts = datetime.now().strftime("%H:%M:%S")
        self.session_log.append(f"[{ts}] {entry}")