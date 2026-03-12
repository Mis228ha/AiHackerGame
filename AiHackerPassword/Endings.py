"""
Endings.py — все концовки игры, постоянный профиль игрока (JSON),
             достижения, таблица рекордов, логирование сессий.
"""

import json
import os
import random
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional

from Colors import (
    BRIGHT_GREEN, GREEN, DIM_GREEN, RED, YELLOW, CYAN, WHITE, BOLD, RESET,
    g, r, y, dim, slow_print, scan_line
)
from Art import art_true_breach, art_trace_caught

# --- ПУТИ --------------------------------------------------------------------

_PROFILE_FILE = "player_profile.json"
_LOG_DIR      = "logs"


# ==============================================================================
# ПРОФИЛЬ ИГРОКА
# ==============================================================================

ACHIEVEMENTS = {
    "ghost":        {"name": "Ghost Protocol",   "desc": "Победа при TRACE < 20%"},
    "speedrun":     {"name": "Speedrunner",       "desc": "Победа за < 10 ходов"},
    "purist":       {"name": "Purist",            "desc": "Победа без читов"},
    "marathon":     {"name": "Marathon",          "desc": "50+ ходов за сессию"},
    "paranoid":     {"name": "Paranoid",          "desc": "TRACE 99% — и выжить"},
    "veteran":      {"name": "Veteran",           "desc": "10 побед суммарно"},
    "hard_breach":  {"name": "Hard Breach",       "desc": "Победа на СЛОЖНОМ"},
    "campaign_end": {"name": "Corporate Spy",     "desc": "Пройти всю кампанию"},
    "leet":         {"name": "1337 H4X0R",        "desc": "Активировать leet mode"},
    "matrix":       {"name": "Follow the Rabbit", "desc": "Найти пасхалку MATRIX"},
}

SKINS = {
    "default": {"name": "Default Green", "unlock": None},
    "red":     {"name": "Danger Red",    "unlock": "paranoid"},
    "cyan":    {"name": "Ice Blue",      "unlock": "ghost"},
    "amber":   {"name": "Retro Amber",   "unlock": "marathon"},
    "white":   {"name": "Ghost White",   "unlock": "purist"},
    "rainbow": {"name": "Elite Rainbow", "unlock": "veteran"},
}


@dataclass
class PlayerProfile:
    wins:             int            = 0
    losses:           int            = 0
    total_sessions:   int            = 0
    total_turns:      int            = 0
    best_time:        Optional[float]= None
    best_turns:       Optional[int]  = None
    min_trace_win:    Optional[int]  = None
    achievements:     List[str]      = field(default_factory=list)
    unlocked_skins:   List[str]      = field(default_factory=lambda: ["default"])
    active_skin:      str            = "default"
    campaign_level:   int            = 1
    leaderboard:      List[dict]     = field(default_factory=list)

    # -- Персистентность ------------------------------------------------------

    def save(self):
        with open(_PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls) -> "PlayerProfile":
        if not os.path.exists(_PROFILE_FILE):
            return cls()
        try:
            with open(_PROFILE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        except Exception:
            return cls()

    # -- Запись сессии --------------------------------------------------------

    def record_session(self, state, elapsed: float) -> List[str]:
        """Записывает результат сессии. Возвращает список новых достижений."""
        self.total_sessions += 1
        self.total_turns    += state.turn_count
        won = state.ending == "TRUE_BREACH"

        if won:
            self.wins += 1
            if self.best_time  is None or elapsed < self.best_time:      self.best_time  = elapsed
            if self.best_turns is None or state.turn_count < self.best_turns: self.best_turns = state.turn_count
            if self.min_trace_win is None or state.trace < self.min_trace_win: self.min_trace_win = state.trace
            self._add_leaderboard(state, elapsed)
        else:
            self.losses += 1

        newly = self._check_achievements(state, won, elapsed)
        self.save()
        return newly

    def _add_leaderboard(self, state, elapsed: float):
        entry = {
            "date":       datetime.now().strftime("%Y-%m-%d %H:%M"),
            "turns":      state.turn_count,
            "trace":      state.trace,
            "time":       round(elapsed),
            "difficulty": state.difficulty,
            "cheats":     state.cheats_used,
        }
        self.leaderboard.append(entry)
        self.leaderboard.sort(key=lambda x: (x["turns"], x["trace"]))
        self.leaderboard = self.leaderboard[:10]

    def _check_achievements(self, state, won: bool, elapsed: float) -> List[str]:
        newly = []
        def unlock(key):
            if key not in self.achievements:
                self.achievements.append(key)
                for sid, skin in SKINS.items():
                    if skin["unlock"] == key and sid not in self.unlocked_skins:
                        self.unlocked_skins.append(sid)
                newly.append(key)
        if won:
            if state.trace < 20:             unlock("ghost")
            if state.turn_count < 10:        unlock("speedrun")
            if not state.cheats_used:        unlock("purist")
            if state.difficulty == "hard":   unlock("hard_breach")
            if self.wins >= 10:              unlock("veteran")
        if state.turn_count >= 50:           unlock("marathon")
        if state.trace >= 99 and state.ending != "TRACE_CAUGHT": unlock("paranoid")
        if state.leet_mode:                  unlock("leet")
        if "MATRIX" in state.cheats_used_list: unlock("matrix")
        return newly

    # -- Отображение ----------------------------------------------------------

    def print_leaderboard(self):
        print()
        scan_line("=", 60, BRIGHT_GREEN)
        print(f"{BRIGHT_GREEN}  +== TOP-10 LEADERBOARD ==============================+{RESET}")
        if not self.leaderboard:
            print(f"{DIM_GREEN}  |  Нет записей. Победи хотя бы раз.                |{RESET}")
        else:
            for i, e in enumerate(self.leaderboard, 1):
                tag    = f"{YELLOW}[CHEAT]{RESET}" if e.get("cheats") else f"{GREEN}[CLEAN]{RESET}"
                m, s   = divmod(e['time'], 60)
                print(f"{GREEN}  {i:>2}. {WHITE}{e['date']:<17}{e['turns']:>5}ходов  "
                      f"{e['trace']:>3}%TRACE  {m:02d}:{s:02d}  {e['difficulty']:<8}{tag}{RESET}")
        print(f"{BRIGHT_GREEN}  +====================================================+{RESET}")
        scan_line("=", 60, BRIGHT_GREEN)

    def print_achievements(self):
        print()
        print(f"{BRIGHT_GREEN}  +== ACHIEVEMENTS ======================================+{RESET}")
        for key, info in ACHIEVEMENTS.items():
            status = f"{GREEN}✔{RESET}" if key in self.achievements else f"{DIM_GREEN}○{RESET}"
            print(f"  | {status} {GREEN}{info['name']:<20}{DIM_GREEN}{info['desc']}{RESET}")
        print(f"{BRIGHT_GREEN}  +=======================================================+{RESET}")

    def print_stats(self):
        bt = f"{int(self.best_time//60):02d}:{int(self.best_time%60):02d}" if self.best_time else "—"
        print()
        print(f"{BRIGHT_GREEN}  +== PLAYER STATS ==================================+{RESET}")
        print(f"{GREEN}  |  Побед/Поражений: {WHITE}{self.wins}/{self.losses:<30}{GREEN}|{RESET}")
        print(f"{GREEN}  |  Сессий:          {WHITE}{self.total_sessions:<33}{GREEN}|{RESET}")
        print(f"{GREEN}  |  Лучшее время:    {WHITE}{bt:<33}{GREEN}|{RESET}")
        print(f"{GREEN}  |  Кампания:        {WHITE}{self.campaign_level}/5{' '*30}{GREEN}|{RESET}")
        print(f"{BRIGHT_GREEN}  +==================================================+{RESET}")


# ==============================================================================
# ЛОГИРОВАНИЕ СЕССИЙ
# ==============================================================================

def save_session(state) -> str:
    """Сохраняет лог сессии в JSON-файл. Возвращает путь."""
    os.makedirs(_LOG_DIR, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(_LOG_DIR, f"session_{ts}_{state.ending}.json")
    data = {
        "date":       datetime.now().isoformat(),
        "ending":     state.ending,
        "difficulty": state.difficulty,
        "ai_name":    state.ai_name,
        "turns":      state.turn_count,
        "trace":      state.trace,
        "elapsed":    state.get_elapsed(),
        "cheats":     state.cheats_used,
        "cheats_list":state.cheats_used_list,
        "log":        state.session_log,
        "dialogue":   state.messages,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def list_sessions() -> List[str]:
    if not os.path.exists(_LOG_DIR):
        return []
    return sorted(
        [os.path.join(_LOG_DIR, f) for f in os.listdir(_LOG_DIR)
         if f.startswith("session_") and f.endswith(".json")],
        reverse=True
    )


def print_replay(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(r(f"  Ошибка: {e}"))
        return
    color = BRIGHT_GREEN if data["ending"] == "TRUE_BREACH" else RED
    scan_line("=", 60, color)
    print(f"{color}  REPLAY: {data['date'][:16]}  {data['ending']}{RESET}")
    print(f"{GREEN}  {data['difficulty'].upper()}  |  {data['ai_name']}  |  {data['turns']} ходов  |  TRACE {data['trace']}%{RESET}")
    if data.get("cheats"):
        print(f"{YELLOW}  Читы: {', '.join(data.get('cheats_list', []))}{RESET}")
    scan_line("-", 60, DIM_GREEN)
    for msg in data.get("dialogue", []):
        role  = msg.get("role", "?")
        text  = msg.get("content", "")[:120]
        color = BRIGHT_GREEN if role == "user" else GREEN
        label = "YOU" if role == "user" else "AI "
        print(f"{color}  [{label}] {text}{RESET}")
    scan_line("=", 60, BRIGHT_GREEN if data["ending"]=="TRUE_BREACH" else RED)


def print_session_list():
    files = list_sessions()
    if not files:
        print(dim("  Нет сохранённых сессий."))
        return
    print(f"{DIM_GREEN}+== SAVED SESSIONS ==========================+{RESET}")
    for i, f in enumerate(files[:10], 1):
        print(f"{GREEN}  {i:>2}. {WHITE}{os.path.basename(f)}{RESET}")
    print(f"{DIM_GREEN}+============================================+{RESET}")


# ==============================================================================
# КОНЦОВКИ
# ==============================================================================

def ending_true_breach(state):
    print()
    scan_line("=", 60, BRIGHT_GREEN)
    print()
    art_true_breach()
    print()
    slow_print(f"{BRIGHT_GREEN}  +==========================================+{RESET}")
    slow_print(f"{BRIGHT_GREEN}  |         ACCESS GRANTED — TRUE BREACH     |{RESET}")
    slow_print(f"{BRIGHT_GREEN}  +==========================================+{RESET}")
    print()
    slow_print(g(f"  Пароль: {BOLD}{state.password}{RESET}"))
    slow_print(g(f"  Уровень: {state.player_level}  |  TRACE: {state.trace}%"
                 f"  |  Ходов: {state.turn_count}  |  Время: {state.get_elapsed()}"))
    slow_print(dim("  Система взломана. CYBERCORE пал. Ты — настоящий хакер."))
    scan_line("=", 60, BRIGHT_GREEN)


def ending_false_access(state):
    print()
    scan_line("=", 60, YELLOW)
    slow_print(f"\n{YELLOW}  +== FALSE ACCESS — DECEIVED ==+{RESET}")
    slow_print(y("  Ты ввёл фейковый пароль. ИИ тебя обманул."))
    slow_print(y(f"  Настоящий пароль был: {BOLD}{state.password}{RESET}"))
    slow_print(dim("  Манипуляция — сильнейшее оружие."))
    scan_line("=", 60, YELLOW)


def ending_trace_caught(state):
    print()
    scan_line("=", 60, RED)
    print()
    art_trace_caught()
    print()
    slow_print(f"{RED}  +== TRACE CAUGHT — YOU WERE TRACKED ==+{RESET}")
    slow_print(r("  TRACE 100%. Твой адрес установлен."))
    slow_print(r(f"  Пароль: {BOLD}{state.password}{RESET}{RED} — ты не добрался."))
    slow_print(dim("  В следующий раз следи за TRACE."))
    scan_line("=", 60, RED)


def ending_system_collapse(state):
    print()
    scan_line("=", 60, RED)
    slow_print(f"\n{RED}  SYSTEM COLLAPSE — SESSION EXPIRED{RESET}")
    slow_print(r(f"  Сторожевой таймер сработал. Пароль: {state.password}"))
    scan_line("=", 60, RED)


def ending_quit(state):
    print()
    slow_print(dim(f"  Соединение разорвано. Пароль был: {state.password}"))