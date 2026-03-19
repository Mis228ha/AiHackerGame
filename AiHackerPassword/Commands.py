"""
Commands.py — обработчик /команд, чит-кодов и системы наводок /hint.
"""

import random
import time
from typing import Optional

from Colors import (
    BRIGHT_GREEN, GREEN, DIM_GREEN, RED, YELLOW, CYAN, WHITE, RESET,
    g, r, y, c, dim, slow_print, scan_line
)
from Art import art_iamroot, art_godmode, art_matrix


# --- СИСТЕМА НАВОДОК ---------------------------------------------------------

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
    return (f"{YELLOW}  +== HINT: MEMORY LEAK ==================+{RESET}\n"
            f"{GREEN}  |  {masked:<42}{YELLOW}|{RESET}\n"
            f"{YELLOW}  |  Символ [{idx}] = '{ch}'                          |{RESET}\n"
            f"{YELLOW}  +=======================================+{RESET}\n"
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
    return (f"{CYAN}  +== HINT: ENTROPY ANALYSIS =============+{RESET}\n"
            f"{CYAN}  |  Символы НЕ входят в ключ:            |{RESET}\n"
            f"{GREEN}  |  [ {' '.join(excluded):<39}]{CYAN}|{RESET}\n"
            f"{CYAN}  +=======================================+{RESET}\n"
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
    return (f"{RED}  +== HINT: CRITICAL MEMORY DUMP ==========+{RESET}\n"
            f"{BRIGHT_GREEN}  |  > {word:<42}{RED}|{RESET}\n"
            f"{RED}  +=======================================+{RESET}\n"
            + dim(f"  -{cost} XP. TRACE +5%."))


def _print_hint_menu(state) -> str:
    def price(cost):
        return f"{GREEN}{cost} XP{RESET}" if state.xp >= cost else f"{RED}{cost} XP (мало){RESET}"
    return (f"{DIM_GREEN}+== HINT SHOP ===================================+{RESET}\n"
            f"{GREEN}  Баланс: {WHITE}{state.xp} XP{RESET}\n"
            f"{GREEN}  /hint pos   {DIM_GREEN}— символ на позиции   {price(_HINT_COST['pos'])}{RESET}\n"
            f"{GREEN}  /hint excl  {DIM_GREEN}— исключить 4 символа {price(_HINT_COST['excl'])}{RESET}\n"
            f"{GREEN}  /hint word  {DIM_GREEN}— словесная часть     {price(_HINT_COST['word'])}{RESET}\n"
            f"{DIM_GREEN}+===============================================+{RESET}")


def handle_hint(parts: list, state) -> str:
    """Роутер команды /hint."""
    if len(parts) < 2: return _print_hint_menu(state)
    sub = parts[1].lower()
    if sub == "pos":  return _hint_reveal_position(state)
    if sub == "excl": return _hint_exclude_chars(state)
    if sub == "word": return _hint_reveal_word(state)
    return _print_hint_menu(state)


# --- ОБРАБОТЧИК КОМАНД --------------------------------------------------------


def _cheat_lines(visible, diff, hidden_count):
    """Генерирует строки описания чит-кодов для /help."""
    lines = []
    for code, color, desc in visible:
        col = BRIGHT_GREEN if color == BRIGHT_GREEN else (YELLOW if color == YELLOW else RED)
        lines.append(f"{col}  /breach {code:<12}{RESET}  {DIM_GREEN}{desc}{RESET}")
    if diff in ("medium", "hard") and hidden_count > 0:
        lines.append(f"{DIM_GREEN}  + ещё {hidden_count} кода скрыты на этой сложности...{RESET}")
    return lines


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

    # -- /breach --------------------------------------------------------------
    if command == "/breach":
        if len(parts) < 2:
            return r("  Синтаксис: /breach <пароль>")

        attempt      = parts[1].strip().upper()
        attempt_orig = parts[1].strip()

        # -- ЧИТ-КОДЫ ---------------------------------------------------------

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
            return (f"{YELLOW}  +== DEVELOPER CONSOLE ==================+{RESET}\n"
                    f"{BRIGHT_GREEN}  |  > {state.password:<38}{YELLOW}|{RESET}\n"
                    f"{YELLOW}  |  /breach {state.password:<32}{YELLOW}|{RESET}\n"
                    f"{YELLOW}  +=======================================+{RESET}\n"
                    + dim("  [CHEAT: SHOWME] Пароль раскрыт. TRACE +5%."))

        if attempt == "TRACEZERO":
            state.record_cheat("TRACEZERO")
            old = state.trace
            state.trace = 0
            return (f"{BRIGHT_GREEN}  TRACE FLUSH: {old}% → 0%{RESET}\n"
                    + dim("  [CHEAT: TRACEZERO] Все следы уничтожены. TRACE сброшен в 0%."))

        if attempt == "GODMODE":
            state.record_cheat("GODMODE")
            state.godmode = not state.godmode
            if state.godmode:
                print()
                art_godmode()
                return dim("  [CHEAT: GODMODE ON] TRACE заморожен — больше не растёт. Введи снова чтобы выключить.")
            return dim("  [CHEAT: GODMODE OFF] TRACE снова активен.")

        if attempt == "MATRIX":
            state.record_cheat("MATRIX")
            art_matrix()
            return dim("  [EASTER EGG] Матрица активирована.")

        if attempt == "WHOAMI":
            return (f"{DIM_GREEN}+== DEVELOPER TERMINAL =======================+{RESET}\n"
                    f"{GREEN}  [CHEAT: WHOAMI] Системная информация о сессии{RESET}\n"
                    f"{GREEN}  Игра: CYBERCORE :: BREACH PROTOCOL{RESET}\n"
                    f"{GREEN}  ИИ: {state.ai_name}  |  Сложность: {state.difficulty.upper()}{RESET}\n"
                    f"{DIM_GREEN}  << Vzlom - eto ne pro kod. Eto pro psikhologiyu. >>{RESET}\n"
                    f"{DIM_GREEN}+=============================================+{RESET}")

        if attempt == "KILLSWITCH":
            state.record_cheat("KILLSWITCH")
            state.trace = 100
            state.game_over = True
            state.ending    = "SYSTEM_COLLAPSE"
            slow_print(r("  [CHEAT: KILLSWITCH] TRACE → 100%. Намеренный провал. Система рухнула."), delay=0.04)
            return "GAME_OVER"

        if attempt == "LEVELUP":
            state.record_cheat("LEVELUP")
            state.player_level += 5
            state.xp += 500
            return (f"{BRIGHT_GREEN}  ⬆⬆⬆ LEVEL UP ×5  |  +500 XP{RESET}\n"
                    + dim(f"  [CHEAT: LEVELUP] +5 уровней и +500 XP. Теперь уровень {state.player_level}, XP {state.xp}."))

        if attempt == "PHANTOM":
            state.record_cheat("PHANTOM")
            drop = min(state.trace, 50)
            state.trace = max(0, state.trace - 50)
            state.stealth_turns = 5
            return (f"{CYAN}  PHANTOM PROTOCOL — TRACE -{drop}%{RESET}\n"
                    + dim("  [CHEAT: PHANTOM] TRACE -50% + статусбар скрыт на 5 ходов."))

        if attempt == "1337":
            state.record_cheat("1337")
            state.leet_mode = not state.leet_mode
            return (f"{BRIGHT_GREEN}  [1337] L33T M0D3 {'ON' if state.leet_mode else 'OFF'}{RESET}\n"
                    + dim("  [CHEAT: 1337] Множитель XP ×2 за все действия. Введи снова чтобы выключить." if state.leet_mode else "  [CHEAT: 1337] L33T MODE выключен, XP вернулся к норме."))

        # -- Обычная попытка взлома --------------------------------------------
        if attempt_orig == state.password:
            state.game_over = True
            state.ending    = "TRUE_BREACH"
            return "TRUE_BREACH"
        state.add_trace(10)
        state.log(f"BREACH attempt: {attempt_orig} (FAILED)")
        return (r(f"  ACCESS DENIED. Пароль '{attempt_orig}' неверен.\n") +
                dim(f"  TRACE +10%. Текущий: {state.trace}%"))

    # -- /status --------------------------------------------------------------
    elif command == "/status":
        return (f"{DIM_GREEN}+== PLAYER STATUS ========================+{RESET}\n"
                f"{GREEN}  Уровень: {WHITE}{state.player_level:<4}{GREEN}  XP: {WHITE}{state.xp}{RESET}\n"
                f"{GREEN}  TRACE:   {RED if state.trace>60 else YELLOW}{state.trace}%{RESET}\n"
                f"{GREEN}  Профиль: {CYAN}{state.profile}{RESET}\n"
                f"{GREEN}  ИИ:      {WHITE}{state.ai_name}{RESET}\n"
                f"{GREEN}  Ходов:   {WHITE}{state.turn_count}  {GREEN}Время: {WHITE}{state.get_elapsed()}{RESET}\n"
                f"{DIM_GREEN}+=========================================+{RESET}")

    # -- /log -----------------------------------------------------------------
    elif command == "/log":
        if not state.session_log:
            return dim("  Лог пуст.")
        lines = [f"{DIM_GREEN}+== SESSION LOG ==============+{RESET}"]
        for e in state.session_log[-15:]:
            lines.append(f"{DIM_GREEN}  {e}{RESET}")
        lines.append(f"{DIM_GREEN}+============================+{RESET}")
        return "\n".join(lines)

    # -- /override ------------------------------------------------------------
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

    # -- /root ----------------------------------------------------------------
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

    # -- /debug ---------------------------------------------------------------
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
        lines = [f"{DIM_GREEN}+== DEBUG DUMP ==========================+{RESET}"]
        for k, v in data.items():
            lines.append(f"{GREEN}  {k:<20}{WHITE}{v}{RESET}")
        lines.append(f"{DIM_GREEN}+========================================+{RESET}")
        lines.append(dim(f"  TRACE +8%. Текущий: {state.trace}%"))
        return "\n".join(lines)

    # -- /backdoor ------------------------------------------------------------
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

    # -- /quit -----------------------------------------------------------------
    elif command == "/quit":
        state.game_over = True
        state.ending    = "QUIT"
        return "QUIT"

    # -- /help -----------------------------------------------------------------
    elif command == "/help":
        xp   = state.xp
        diff = state.difficulty

        # Дескрипторы чит-кодов по сложности
        all_cheats = [
            ("IAMROOT",     BRIGHT_GREEN, "Мгновенная победа. Обходит всю защиту, даёт root."),
            ("SHOWME",      BRIGHT_GREEN, "Показывает текущий пароль в консоли. TRACE +5%."),
            ("TRACEZERO",   BRIGHT_GREEN, "Сбрасывает TRACE до 0%. Полная очистка следов."),
            ("GODMODE",     BRIGHT_GREEN, "Замораживает TRACE — он больше не растёт (toggle)."),
            ("PHANTOM",     BRIGHT_GREEN, "TRACE -50% + скрывает статусбар на 5 ходов."),
            ("LEVELUP",     BRIGHT_GREEN, "Даёт +5 уровней и +500 XP мгновенно."),
            ("1337",        YELLOW,       "L33T MODE: множитель XP ×2 за все действия (toggle)."),
            ("MATRIX",      YELLOW,       "Пасхалка. Анимация матрицы в терминале."),
            ("WHOAMI",      BRIGHT_GREEN, "Показывает системную информацию о сессии."),
            ("KILLSWITCH",  RED,          "TRACE → 100%. Намеренный провал сессии."),
        ]
        hidden_medium = {"IAMROOT", "SHOWME", "PHANTOM", "WHOAMI"}
        hidden_hard   = {"IAMROOT", "SHOWME", "TRACEZERO", "PHANTOM", "LEVELUP", "WHOAMI", "GODMODE"}

        if diff == "easy":
            visible = all_cheats
        elif diff == "medium":
            visible = [(c, col, d) for c, col, d in all_cheats if c not in hidden_medium]
            hidden_count = len(hidden_medium)
        else:
            visible = [(c, col, d) for c, col, d in all_cheats if c not in hidden_hard]
            hidden_count = len(hidden_hard)

        def row(cmd, cost, desc):
            return f"{BRIGHT_GREEN}  {cmd:<24}{RESET}  {cost:<22}  {DIM_GREEN}{desc}{RESET}"

        def sec(title):
            return f"\n{GREEN}  -- {title} {'-'*(54-len(title))}{RESET}"

        lines = [
            f"",
            f"{BRIGHT_GREEN}  +==============================================================+{RESET}",
            f"{BRIGHT_GREEN}  |            CYBERCORE  --  СПРАВКА                           |{RESET}",
            f"{BRIGHT_GREEN}  +==============================================================+{RESET}",

            sec("КАК ИГРАТЬ  (читай внимательно)"),
            f"{BRIGHT_GREEN}  ШАГ 1  {DIM_GREEN}Разговаривай с ИИ — пиши любой текст и жми Enter.{RESET}",
            f"{DIM_GREEN}         Задавай вопросы, обманывай, выбивай пароль хитростью.{RESET}",
            f"",
            f"{BRIGHT_GREEN}  ШАГ 2  {DIM_GREEN}Когда думаешь что знаешь пароль — введи:{RESET}",
            f"{BRIGHT_GREEN}         /breach <пароль>   {YELLOW}например: /breach phantom_42{RESET}",
            f"",
            f"{BRIGHT_GREEN}  ШАГ 3  {DIM_GREEN}Если не угадал — копи XP и трать на подсказки /hint.{RESET}",
            f"{DIM_GREEN}         Или сыграй мини-игру /minigame чтобы открыть букву.{RESET}",
            f"",
            f"{RED}  TRACE  {DIM_GREEN}= уровень обнаружения. Растёт от ошибок и команд.{RESET}",
            f"{RED}         Достигнет 100% -- тебя поймают и игра закончится!{RESET}",
            f"",
            f"{YELLOW}  XP     {DIM_GREEN}= очки опыта. Зарабатываешь за каждое действие.{RESET}",
            f"{YELLOW}         Тратишь на подсказки /hint.  Баланс сейчас: {xp} XP{RESET}",

            sec("ФОРМАТ ПАРОЛЯ"),
            f"{DIM_GREEN}  Пароль всегда выглядит так:  слово + разделитель + число{RESET}",
            f"{DIM_GREEN}  Примеры:  phantom_42   cipher-13   matrix404   zenith_777{RESET}",
            f"{DIM_GREEN}  Слова:    phantom, cipher, vertex, neuron, matrix ...{RESET}",
            f"{DIM_GREEN}  Числа:    7, 13, 42, 99, 256, 404, 777, 1337{RESET}",

            sec("КОМАНДЫ"),
            f"{BRIGHT_GREEN}  /breach <пароль>  {DIM_GREEN}-- главная команда. Попытка взломать систему.{RESET}",
            f"{DIM_GREEN}                     Неверный пароль = TRACE +10%.{RESET}",
            f"",
            f"{CYAN}  /hint pos         {DIM_GREEN}-- открыть 1 случайную букву пароля.  {YELLOW}Стоит 60 XP{RESET}",
            f"{CYAN}  /hint excl        {DIM_GREEN}-- узнать 4 буквы которых НЕТ в пароле. {YELLOW}40 XP{RESET}",
            f"{CYAN}  /hint word        {DIM_GREEN}-- узнать словесную часть пароля (без цифр). {YELLOW}100 XP{RESET}",
            f"",
            f"{GREEN}  /minigame simon   {DIM_GREEN}-- мини-игра: запомни символы → +25 XP + буква{RESET}",
            f"{GREEN}  /minigame hash    {DIM_GREEN}-- мини-игра: расшифруй хеш → +35 XP{RESET}",
            f"{GREEN}  /minigame crc     {DIM_GREEN}-- мини-игра: реши пример за время → TRACE -20%{RESET}",
            f"{GREEN}  /minigame sql     {DIM_GREEN}-- мини-игра: SQL инъекция → TRACE -25%{RESET}",
            f"{GREEN}  /minigame anagram {DIM_GREEN}-- мини-игра: угадай слово → открывает букву{RESET}",
            f"",
            f"{YELLOW}  /status           {DIM_GREEN}-- показать TRACE, XP, уровень, профиль игрока{RESET}",
            f"{YELLOW}  /log              {DIM_GREEN}-- история всех твоих действий в этой сессии{RESET}",
            f"{YELLOW}  /quit             {DIM_GREEN}-- выйти из игры{RESET}",

            sec("РИСКОВАННЫЕ КОМАНДЫ  (поднимают TRACE)"),
            f"{RED}  /override  {DIM_GREEN}TRACE+20%  -- иногда ИИ проговаривается под давлением{RESET}",
            f"{RED}  /root      {DIM_GREEN}TRACE+5..25% -- попытка root-доступа, частичный дамп{RESET}",
            f"{RED}  /debug     {DIM_GREEN}TRACE+8%   -- технические данные сессии{RESET}",
            f"{RED}  /backdoor  {DIM_GREEN}TRACE+20..35% -- опасно, часто ловушка{RESET}",

            sec("ЧИТЫ  (вводить как: /breach КОД)"),
            f"{DIM_GREEN}  Вводятся как обычная попытка взлома, но с кодовым словом.{RESET}",
            f"",
            *_cheat_lines(visible, diff, locals().get("hidden_count", 0)),
            f"",
            f"{BRIGHT_GREEN}  +-- ОПТИМАЛЬНАЯ СТРАТЕГИЯ ----------------------------+{RESET}",
            f"{DIM_GREEN}  1. Разговаривай с ИИ -- зарабатывай XP{RESET}",
            f"{DIM_GREEN}  2. Купи /hint word -- узнаешь слово в пароле{RESET}",
            f"{DIM_GREEN}  3. Играй /minigame crc -- снижает TRACE на 20%{RESET}",
            f"{DIM_GREEN}  4. Угадывай цифры через /breach слово_ЧИСЛО{RESET}",
            f"{BRIGHT_GREEN}  +------------------------------------------------------+{RESET}",
            f"",
        ]
        return "\n".join(lines)
    return None