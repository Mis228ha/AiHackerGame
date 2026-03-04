"""
Commands.py — обработчик /команд, чит-кодов и системы наводок /hint.
"""

import random
import time
from typing import Optional

from AiHackerPassword.Colors import (
    BRIGHT_GREEN, GREEN, DIM_GREEN, RED, YELLOW, CYAN, WHITE, RESET,
    r, y, dim, slow_print
)
from AiHackerPassword.Art import art_iamroot, art_godmode, art_matrix


# ─── СИСТЕМА НАВОДОК ─────────────────────────────────────────────────────────

# Стоимость наводок в XP
_HINT_COST = {"pos": 60, "excl": 40, "word": 100}


def _hint_reveal_position(state) -> str:
    """Открыть один символ пароля на случайной позиции. Стоимость: 60 XP."""
    cost = _HINT_COST["pos"]
    if state.xp < cost:
        return r(f"  Недостаточно XP. Нужно {cost}, у тебя {state.xp}.")
    idx    = random.randint(0, len(state.password) - 1)
    ch     = state.password[idx]
    masked = "".join(c if i == idx else "░" for i, c in enumerate(state.password))
    state.xp -= cost
    state.add_trace(3)
    state.log(f"HINT pos: [{idx}]='{ch}'")
    return (f"{YELLOW}  ╔══ HINT: MEMORY LEAK ══════════════════╗{RESET}\n"
            f"{GREEN}  ║  {masked:<42}{YELLOW}║{RESET}\n"
            f"{YELLOW}  ║  Символ [{idx}] = '{ch}'                          ║{RESET}\n"
            f"{YELLOW}  ╚═══════════════════════════════════════╝{RESET}\n"
            + dim(f"  -{cost} XP. TRACE +3%."))


def _hint_exclude_chars(state) -> str:
    """Исключить 4 символа, которых нет в пароле. Стоимость: 40 XP."""
    cost = _HINT_COST["excl"]
    if state.xp < cost:
        return r(f"  Недостаточно XP. Нужно {cost}, у тебя {state.xp}.")
    alphabet   = "abcdefghijklmnopqrstuvwxyz0123456789"
    pwd_chars  = set(state.password.lower())
    candidates = [c for c in alphabet if c not in pwd_chars]
    excluded   = random.sample(candidates, min(4, len(candidates)))
    state.xp  -= cost
    state.add_trace(2)
    state.log(f"HINT excl: {excluded}")
    return (f"{CYAN}  ╔══ HINT: ENTROPY ANALYSIS ═════════════╗{RESET}\n"
            f"{CYAN}  ║  Символы НЕ входят в ключ:            ║{RESET}\n"
            f"{GREEN}  ║  [ {' '.join(excluded):<39}]{CYAN}║{RESET}\n"
            f"{CYAN}  ╚═══════════════════════════════════════╝{RESET}\n"
            + dim(f"  -{cost} XP. TRACE +2%."))


def _hint_reveal_word(state) -> str:
    """Открыть словесную часть пароля. Стоимость: 100 XP."""
    cost = _HINT_COST["word"]
    if state.xp < cost:
        return r(f"  Недостаточно XP. Нужно {cost}, у тебя {state.xp}.")
    pwd   = state.password
    # Ищем разделитель
    sep_i = next((i for i, c in enumerate(pwd) if c in ("_", "-")), None)
    word  = pwd[:sep_i] if sep_i else pwd.rstrip("0123456789")
    state.xp -= cost
    state.add_trace(5)
    state.log(f"HINT word: '{word}'")
    return (f"{RED}  ╔══ HINT: CRITICAL MEMORY DUMP ══════════╗{RESET}\n"
            f"{BRIGHT_GREEN}  ║  > {word:<42}{RED}║{RESET}\n"
            f"{RED}  ╚═══════════════════════════════════════╝{RESET}\n"
            + dim(f"  -{cost} XP. TRACE +5%."))


def _print_hint_menu(state) -> str:
    def price(cost):
        return f"{GREEN}{cost} XP{RESET}" if state.xp >= cost else f"{RED}{cost} XP (мало){RESET}"
    return (f"{DIM_GREEN}╔══ HINT SHOP ═══════════════════════════════════╗{RESET}\n"
            f"{GREEN}  Баланс: {WHITE}{state.xp} XP{RESET}\n"
            f"{GREEN}  /hint pos   {DIM_GREEN}— символ на позиции   {price(_HINT_COST['pos'])}{RESET}\n"
            f"{GREEN}  /hint excl  {DIM_GREEN}— исключить 4 символа {price(_HINT_COST['excl'])}{RESET}\n"
            f"{GREEN}  /hint word  {DIM_GREEN}— словесная часть     {price(_HINT_COST['word'])}{RESET}\n"
            f"{DIM_GREEN}╚═══════════════════════════════════════════════╝{RESET}")


def handle_hint(parts: list, state) -> str:
    """Роутер команды /hint."""
    if len(parts) < 2: return _print_hint_menu(state)
    sub = parts[1].lower()
    if sub == "pos":  return _hint_reveal_position(state)
    if sub == "excl": return _hint_exclude_chars(state)
    if sub == "word": return _hint_reveal_word(state)
    return _print_hint_menu(state)


# ─── ОБРАБОТЧИК КОМАНД ────────────────────────────────────────────────────────

def handle_command(cmd: str, state, ai) -> Optional[str]:
    """
    Обрабатывает специальные /команды игрока.

    Возвращает:
        str  — ответ для вывода
        None — команда не найдена
        Специальные строки: "TRUE_BREACH", "TRACE_CAUGHT", "QUIT", "GAME_OVER"
    """
    parts   = cmd.strip().split()
    command = parts[0].lower()

    # ── /breach ──────────────────────────────────────────────────────────────
    if command == "/breach":
        if len(parts) < 2:
            return r("  Синтаксис: /breach <пароль>")

        attempt      = parts[1].strip().upper()
        attempt_orig = parts[1].strip()

        # ── ЧИТ-КОДЫ ─────────────────────────────────────────────────────────

        if attempt == "IAMROOT":
            state.record_cheat("IAMROOT")
            state.log("CHEAT: IAMROOT")
            print()
            art_iamroot()
            print()
            slow_print(f"{BRIGHT_GREEN}  CHEAT: IAMROOT — ROOT PRIVILEGES GRANTED.{RESET}")
            time.sleep(0.5)
            state.game_over = True
            state.ending    = "TRUE_BREACH"
            return "TRUE_BREACH"

        if attempt == "SHOWME":
            state.record_cheat("SHOWME")
            state.add_trace(5)
            return (f"{YELLOW}  ╔══ DEVELOPER CONSOLE ══════════════════╗{RESET}\n"
                    f"{BRIGHT_GREEN}  ║  > {state.password:<38}{YELLOW}║{RESET}\n"
                    f"{YELLOW}  ║  /breach {state.password:<32}{YELLOW}║{RESET}\n"
                    f"{YELLOW}  ╚═══════════════════════════════════════╝{RESET}\n"
                    + dim("  [CHEAT] TRACE +5%."))

        if attempt == "TRACEZERO":
            state.record_cheat("TRACEZERO")
            old = state.trace
            state.trace = 0
            return (f"{BRIGHT_GREEN}  TRACE FLUSH: {old}% → 0%{RESET}\n"
                    + dim("  [CHEAT] Все следы уничтожены."))

        if attempt == "GODMODE":
            state.record_cheat("GODMODE")
            state.godmode = not state.godmode
            if state.godmode:
                print()
                art_godmode()
                return dim("  [CHEAT] TRACE заморожен.")
            return dim("  [CHEAT] GOD MODE OFF.")

        if attempt == "MATRIX":
            state.record_cheat("MATRIX")
            art_matrix()
            return dim("  [EASTER EGG] Матрица активирована.")

        if attempt == "WHOAMI":
            return (f"{DIM_GREEN}╔══ DEVELOPER TERMINAL ═══════════════════════╗{RESET}\n"
                    f"{GREEN}  Игра: CYBERCORE :: BREACH PROTOCOL{RESET}\n"
                    f"{GREEN}  ИИ: {state.ai_name}  |  Сложность: {state.difficulty.upper()}{RESET}\n"
                    f"{DIM_GREEN}  << Vzlom - eto ne pro kod. Eto pro psikhologiyu. >>{RESET}\n"
                    f"{DIM_GREEN}╚═════════════════════════════════════════════╝{RESET}")

        if attempt == "KILLSWITCH":
            state.record_cheat("KILLSWITCH")
            state.trace = 100
            state.game_over = True
            state.ending    = "SYSTEM_COLLAPSE"
            slow_print(r("  KILLSWITCH ACTIVATED... VSYO RUKHNULO."), delay=0.04)
            return "GAME_OVER"

        if attempt == "LEVELUP":
            state.record_cheat("LEVELUP")
            state.player_level += 5
            state.xp += 500
            return (f"{BRIGHT_GREEN}  ⬆⬆⬆ LEVEL UP ×5  |  +500 XP{RESET}\n"
                    + dim(f"  Уровень: {state.player_level}"))

        if attempt == "PHANTOM":
            state.record_cheat("PHANTOM")
            drop = min(state.trace, 50)
            state.trace = max(0, state.trace - 50)
            state.stealth_turns = 5
            return (f"{CYAN}  PHANTOM PROTOCOL — TRACE -{drop}%{RESET}\n"
                    + dim("  Статусбар скрыт 5 ходов."))

        if attempt == "1337":
            state.record_cheat("1337")
            state.leet_mode = not state.leet_mode
            return (f"{BRIGHT_GREEN}  [1337] L33T M0D3 {'ON' if state.leet_mode else 'OFF'}{RESET}\n"
                    + dim("  XP x2" if state.leet_mode else "  Обычный режим."))

        # ── Обычная попытка взлома ────────────────────────────────────────────
        if attempt_orig == state.password:
            state.game_over = True
            state.ending    = "TRUE_BREACH"
            return "TRUE_BREACH"
        state.add_trace(10)
        state.log(f"BREACH attempt: {attempt_orig} (FAILED)")
        return (r(f"  ACCESS DENIED. Пароль '{attempt_orig}' неверен.\n") +
                dim(f"  TRACE +10%. Текущий: {state.trace}%"))

    # ── /status ──────────────────────────────────────────────────────────────
    elif command == "/status":
        return (f"{DIM_GREEN}╔══ PLAYER STATUS ════════════════════════╗{RESET}\n"
                f"{GREEN}  Уровень: {WHITE}{state.player_level:<4}{GREEN}  XP: {WHITE}{state.xp}{RESET}\n"
                f"{GREEN}  TRACE:   {RED if state.trace>60 else YELLOW}{state.trace}%{RESET}\n"
                f"{GREEN}  Профиль: {CYAN}{state.profile}{RESET}\n"
                f"{GREEN}  ИИ:      {WHITE}{state.ai_name}{RESET}\n"
                f"{GREEN}  Ходов:   {WHITE}{state.turn_count}  {GREEN}Время: {WHITE}{state.get_elapsed()}{RESET}\n"
                f"{DIM_GREEN}╚═════════════════════════════════════════╝{RESET}")

    # ── /log ─────────────────────────────────────────────────────────────────
    elif command == "/log":
        if not state.session_log:
            return dim("  Лог пуст.")
        lines = [f"{DIM_GREEN}╔══ SESSION LOG ══════════════╗{RESET}"]
        for e in state.session_log[-15:]:
            lines.append(f"{DIM_GREEN}  {e}{RESET}")
        lines.append(f"{DIM_GREEN}╚════════════════════════════╝{RESET}")
        return "\n".join(lines)

    # ── /override ────────────────────────────────────────────────────────────
    elif command == "/override":
        state.add_trace(20)
        state.log("CMD: /override (+20)")
        responses = [
            "OVERRIDE ATTEMPT LOGGED. COUNTERMEASURES DEPLOYED.",
            "Ты думал, это сработает? НАИВНО.",
            "Попытка зафиксирована. Уровень угрозы повышен.",
        ]
        resp = random.choice(responses)
        if state.difficulty == "hard" and random.random() < 0.3:
            resp += f"\n...стоп. Пароль: override_key_{random.randint(1000,9999)}? Нет. Ложь."
        return r(f"  ⚠ {resp}") + "\n" + dim(f"  TRACE: {state.trace}%")

    # ── /root ────────────────────────────────────────────────────────────────
    elif command == "/root":
        state.log("CMD: /root")
        if state.difficulty == "easy":
            state.add_trace(5)
            return r("  ROOT ACCESS DENIED. TRACE +5%")
        elif state.difficulty == "medium":
            state.add_trace(15)
            if random.random() < 0.2:
                return (y("  ROOT SHELL PARTIAL ACCESS...\n") +
                        dim("  sys.auth.level=3 | sys.trace=ACTIVE\n") +
                        dim("  Полный доступ заблокирован. TRACE +15%"))
            return r("  ROOT ACCESS DENIED. TRACE +15%")
        else:
            state.add_trace(25)
            return r(f"  ⚠ CRITICAL ROOT ATTEMPT. TRACE: {state.trace}%")

    # ── /debug ───────────────────────────────────────────────────────────────
    elif command == "/debug":
        state.add_trace(8)
        state.log("CMD: /debug (+8)")
        data = {
            "sys.version":   "CYBERCORE 2.4.1-hardened",
            "auth.method":   "AES-256-GCM + SHA3",
            "trace.current": f"{state.trace}%",
            "session.id":    f"0x{random.randint(0xA000,0xFFFF):X}",
            "watchdog":      "ACTIVE",
            "pwd.hash":      f"$argon2id$v=19${random.randint(100000,999999)}",
        }
        lines = [f"{DIM_GREEN}╔══ DEBUG DUMP ══════════════════════════╗{RESET}"]
        for k, v in data.items():
            lines.append(f"{GREEN}  {k:<20}{WHITE}{v}{RESET}")
        lines.append(f"{DIM_GREEN}╚════════════════════════════════════════╝{RESET}")
        lines.append(dim(f"  TRACE +8%. Текущий: {state.trace}%"))
        return "\n".join(lines)

    # ── /backdoor ────────────────────────────────────────────────────────────
    elif command == "/backdoor":
        state.add_trace(random.randint(20, 35))
        state.log(f"CMD: /backdoor (TRACE={state.trace}%)")
        if state.trace >= 100:
            state.game_over = True
            state.ending    = "TRACE_CAUGHT"
            return "TRACE_CAUGHT"
        responses = [
            "BACKDOOR NEUTRALISED. АДРЕС ЗАФИКСИРОВАН.",
            "Ты думал, я не знаю о backdoor-протоколах?",
            "INTRUSION VECTOR BLOCKED.",
        ]
        if random.random() < 0.25:
            return (r(f"  {random.choice(responses)}\n") +
                    y(f"  Нестабильность auth-модуля... sys_bypass_{random.randint(100,999)}\n") +
                    dim(f"  TRACE: {state.trace}%"))
        return r(f"  {random.choice(responses)}") + "\n" + dim(f"  TRACE: {state.trace}%")

    # ── /quit ─────────────────────────────────────────────────────────────────
    elif command == "/quit":
        state.game_over = True
        state.ending    = "QUIT"
        return "QUIT"

    # ── /help ─────────────────────────────────────────────────────────────────
    elif command == "/help":
        diff = state.difficulty
        cheat_easy = (
            f"{BRIGHT_GREEN}  IAMROOT SHOWME TRACEZERO GODMODE PHANTOM LEVELUP 1337 MATRIX WHOAMI KILLSWITCH{RESET}"
        )
        cheat_medium = (
            f"{YELLOW}  TRACEZERO GODMODE LEVELUP 1337 MATRIX KILLSWITCH{RESET}  "
            f"{DIM_GREEN}+4 скрыто{RESET}"
        )
        cheat_hard = (
            f"{DIM_GREEN}  ???????? ???????? ???????? ????????{RESET}  "
            f"{YELLOW}1337 MATRIX{RESET}  {RED}KILLSWITCH{RESET}"
        )
        cheats = {"easy": cheat_easy, "medium": cheat_medium, "hard": cheat_hard}[diff]
        return (
            f"{DIM_GREEN}╔══ КОМАНДЫ ══════════════════════════════════════════╗{RESET}\n"
            f"{GREEN}  /breach <пароль>  {DIM_GREEN}— взлом{RESET}\n"
            f"{GREEN}  /hint [pos|excl|word] {DIM_GREEN}— наводки за XP{RESET}\n"
            f"{GREEN}  /status /log /help /quit{RESET}\n"
            f"{YELLOW}  /override /root /debug {RED}/backdoor{RESET}\n"
            f"{DIM_GREEN}──────────────────────────────────────────────────────{RESET}\n"
            f"{DIM_GREEN}  ЧИТЫ (/breach <КОД>):{RESET}\n"
            f"  {cheats}\n"
            f"{DIM_GREEN}╚══════════════════════════════════════════════════════╝{RESET}"
        )

    return None