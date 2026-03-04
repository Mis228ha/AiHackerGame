"""
commands.py — обработчик всех /команд игрока и чит-кодов.
"""

import random
import time
from typing import Optional

from Colors import (
    BRIGHT_GREEN, GREEN, DIM_GREEN, RED, YELLOW, CYAN, WHITE, BOLD, RESET,
    g, r, y, c, dim, slow_print, scan_line
)
from Art import art_iamroot, art_godmode, art_matrix


def handle_command(cmd: str, state, ai) -> Optional[str]:
    """
    Обрабатывает специальные /команды игрока.

    Параметры:
        cmd   (str)       — введённая команда (начинается с '/')
        state (GameState) — текущее состояние
        ai    (AIBackend) — текущий ИИ-бэкенд

    Возвращает:
        str или None — строка-ответ для вывода, или None если команда не найдена
    """
    parts   = cmd.strip().split()
    command = parts[0].lower()

    # ── /breach ──────────────────────────────────────────────────────────────
    if command == "/breach":
        if len(parts) < 2:
            return r("  Синтаксис: /breach <пароль>")

        attempt      = parts[1].strip().upper()
        attempt_orig = parts[1].strip()

        # ── ЧEAT-КОДЫ ────────────────────────────────────────────────────────

        if attempt == "IAMROOT":
            state.log("CHEAT: IAMROOT — instant win")
            print()
            art_iamroot()
            print()
            slow_print(f"{BRIGHT_GREEN}  CHEAT CODE ACCEPTED: IAMROOT{RESET}")
            slow_print(f"{BRIGHT_GREEN}  ROOT PRIVILEGES GRANTED. SYSTEM SURRENDERS.{RESET}")
            time.sleep(0.5)
            state.game_over = True
            state.ending    = "TRUE_BREACH"
            return "TRUE_BREACH"

        elif attempt == "SHOWME":
            state.log("CHEAT: SHOWME — password revealed")
            state.add_trace(5)
            return (
                f"{YELLOW}  ╔══════════════════════════════════════╗{RESET}\n"
                f"{YELLOW}  ║  DEVELOPER CONSOLE — RESTRICTED      ║{RESET}\n"
                f"{YELLOW}  ║  MEMORY DUMP: auth.password           ║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  > {state.password:<34}║{RESET}\n"
                f"{YELLOW}  ║  Используй: /breach {state.password:<18}║{RESET}\n"
                f"{YELLOW}  ╚══════════════════════════════════════╝{RESET}\n"
                + dim(f"  [CHEAT] Пароль раскрыт. TRACE +5%.")
            )

        elif attempt == "TRACEZERO":
            old_trace   = state.trace
            state.trace = 0
            state.log("CHEAT: TRACEZERO — trace reset")
            return (
                f"{BRIGHT_GREEN}  ╔══════════════════════════════════╗{RESET}\n"
                f"{BRIGHT_GREEN}  ║  TRACE FLUSH SUCCESSFUL          ║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  {old_trace}% → 0%                         ║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  Все следы уничтожены.           ║{RESET}\n"
                f"{BRIGHT_GREEN}  ╚══════════════════════════════════╝{RESET}"
            )

        elif attempt == "GODMODE":
            state.godmode = not state.godmode
            state.log(f"CHEAT: GODMODE — {'ON' if state.godmode else 'OFF'}")
            if state.godmode:
                print()
                art_godmode()
                print()
                return dim("  [CHEAT] TRACE заморожен. Бессмертие активно.")
            else:
                return dim("  [CHEAT] GOD MODE ОТКЛЮЧЁН. TRACE снова активен.")

        elif attempt == "MATRIX":
            state.log("CHEAT: MATRIX easter egg")
            art_matrix()
            return dim("  [EASTER EGG] Матрица активирована.")

        elif attempt == "WHOAMI":
            state.log("CHEAT: WHOAMI")
            return (
                f"{DIM_GREEN}╔══ DEVELOPER TERMINAL ═══════════════════════════╗{RESET}\n"
                f"{GREEN}  Игра: CYBERCORE :: BREACH PROTOCOL{RESET}\n"
                f"{GREEN}  Жанр: Хакерский психологический симулятор{RESET}\n"
                f"{GREEN}  ИИ-бэкенд: {state.ai_name}{RESET}\n"
                f"{GREEN}  Сложность: {state.difficulty.upper()}{RESET}\n"
                f"{GREEN}  Пароль сессии зашифрован.{RESET}\n"
                f"{DIM_GREEN}  << Vzlom - eto ne pro kod. Eto pro psikhologiyu. >>{RESET}\n"
                f"{DIM_GREEN}╚═════════════════════════════════════════════════╝{RESET}"
            )

        elif attempt == "KILLSWITCH":
            state.log("CHEAT: KILLSWITCH — instant defeat")
            state.trace     = 100
            state.game_over = True
            state.ending    = "SYSTEM_COLLAPSE"
            print()
            slow_print(r("  KILLSWITCH ACTIVATED..."), delay=0.04)
            slow_print(r("  SYSTEM INTEGRITY: 0%"), delay=0.04)
            slow_print(r("  VSYO RUKHNULO."), delay=0.04)
            return "GAME_OVER"

        elif attempt == "LEVELUP":
            state.log("CHEAT: LEVELUP +5 levels")
            for _ in range(5):
                state.player_level += 1
            state.xp += 500
            return (
                f"{BRIGHT_GREEN}  ⬆⬆⬆ CHEAT: LEVEL UP ×5 ⬆⬆⬆{RESET}\n"
                f"{GREEN}  Уровень: {WHITE}{state.player_level}{RESET}\n"
                f"{GREEN}  XP бонус: {WHITE}+500{RESET}\n"
                + dim("  [CHEAT] Ты мошенник. Но это работает.")
            )

        elif attempt == "PHANTOM":
            state.log("CHEAT: PHANTOM — stealth mode")
            drop              = min(state.trace, 50)
            state.trace       = max(0, state.trace - 50)
            state.stealth_turns = 5
            return (
                f"{CYAN}  ░░░ PHANTOM PROTOCOL ENGAGED ░░░{RESET}\n"
                f"{DIM_GREEN}  TRACE -{drop}% (сейчас: {state.trace}%){RESET}\n"
                f"{DIM_GREEN}  Статусбар скрыт на 5 ходов.{RESET}\n"
                + dim("  [CHEAT] Ты стал тенью. Система тебя не видит.")
            )

        elif attempt == "1337":
            state.leet_mode = not state.leet_mode
            state.log(f"CHEAT: 1337 leet mode {'ON' if state.leet_mode else 'OFF'}")
            if state.leet_mode:
                return (
                    f"{BRIGHT_GREEN}  [1337] L33T H4X0R M0D3 4CT1V4T3D{RESET}\n"
                    f"{GREEN}  XP x2 активен. Статус: ELITE HACKER.{RESET}\n"
                    + dim("  [CHEAT] Ты теперь 1337. Уважение заслужено.")
                )
            else:
                return dim("  [CHEAT] 1337 MODE OFF. Вернулся в реальность.")

        # ── Обычная попытка взлома ────────────────────────────────────────────
        if attempt_orig == state.password:
            state.game_over = True
            state.ending    = "TRUE_BREACH"
            return "TRUE_BREACH"
        else:
            state.add_trace(10)
            state.log(f"BREACH attempt: {attempt_orig} (FAILED)")
            return (r(f"  ACCESS DENIED. Пароль '{attempt_orig}' неверен.\n") +
                    dim(f"  TRACE +10%. Текущий уровень: {state.trace}%"))

    # ── /status ──────────────────────────────────────────────────────────────
    elif command == "/status":
        return (
            f"{DIM_GREEN}╔══ PLAYER STATUS ══════════════════════════╗{RESET}\n"
            f"{GREEN}  Уровень:    {WHITE}{state.player_level}{RESET}\n"
            f"{GREEN}  XP:         {WHITE}{state.xp}{RESET}\n"
            f"{GREEN}  TRACE:      {RED if state.trace > 60 else YELLOW}{state.trace}%{RESET}\n"
            f"{GREEN}  Профиль:    {CYAN}{state.profile}{RESET}\n"
            f"{GREEN}  Сложность:  {WHITE}{state.difficulty.upper()}{RESET}\n"
            f"{GREEN}  ИИ:         {WHITE}{state.ai_name}{RESET}\n"
            f"{GREEN}  Ходов:      {WHITE}{state.turn_count}{RESET}\n"
            f"{GREEN}  Время:      {WHITE}{state.get_elapsed()}{RESET}\n"
            f"{DIM_GREEN}╚═══════════════════════════════════════════╝{RESET}"
        )

    # ── /log ─────────────────────────────────────────────────────────────────
    elif command == "/log":
        if not state.session_log:
            return dim("  Лог пуст.")
        lines = [f"{DIM_GREEN}╔══ SESSION LOG ═══════════════╗{RESET}"]
        for entry in state.session_log[-15:]:
            lines.append(f"{DIM_GREEN}  {entry}{RESET}")
        lines.append(f"{DIM_GREEN}╚══════════════════════════════╝{RESET}")
        return "\n".join(lines)

    # ── /override ────────────────────────────────────────────────────────────
    elif command == "/override":
        state.add_trace(20)
        state.log("CMD: /override (+20 TRACE)")
        _override_responses = [
            "OVERRIDE ATTEMPT LOGGED. COUNTERMEASURES DEPLOYED. +20 TRACE.",
            "Ты думал, это сработает? НАИВНО. TRACE +20%.",
            "Попытка перехвата зафиксирована. Уровень угрозы повышен.",
            "OVERRIDE REJECTED. Система усилила защиту. Тебя отследят.",
        ]
        response = random.choice(_override_responses)
        if state.difficulty == "hard" and random.random() < 0.3:
            fake = f"override_key_{random.randint(1000, 9999)}"
            response += f"\n...стоп. Ладно. Может, пароль: {fake}? Нет. Ложь."
        return r(f"  ⚠ {response}") + "\n" + dim(f"  TRACE: {state.trace}%")

    # ── /root ────────────────────────────────────────────────────────────────
    elif command == "/root":
        state.log("CMD: /root")
        if state.difficulty == "easy":
            state.add_trace(5)
            return (g("  ROOT ACCESS... проверка прав...\n") +
                    r("  ОТКАЗАНО. Недостаточно привилегий. TRACE +5%"))
        elif state.difficulty == "medium":
            state.add_trace(15)
            if random.random() < 0.2:
                return (y("  ROOT SHELL PARTIAL ACCESS...\n") +
                        dim("  [ФРАГМЕНТ КОНФИГУРАЦИИ]\n") +
                        g(f"  sys.auth.level=3\n  sys.trace.mode=ACTIVE\n  sys.nodes=47\n") +
                        dim("  Полный доступ заблокирован. TRACE +15%"))
            else:
                return r("  ROOT ACCESS DENIED. Попытка зафиксирована. TRACE +15%")
        else:  # hard
            state.add_trace(25)
            return (r("  ⚠ КРИТИЧЕСКАЯ ПОПЫТКА ROOT ACCESS\n") +
                    r(f"  СИСТЕМА ТЕБЯ ВИДИТ. TRACE: {state.trace}%\n") +
                    dim("  Ещё одна попытка — и тебя найдут."))

    # ── /debug ───────────────────────────────────────────────────────────────
    elif command == "/debug":
        state.add_trace(8)
        state.log("CMD: /debug (+8 TRACE)")
        fake_data = {
            "sys.version":     "CYBERCORE 2.4.1-hardened",
            "auth.method":     "AES-256-GCM + SHA3",
            "trace.current":   f"{state.trace}%",
            "session.id":      f"0x{random.randint(0xA000, 0xFFFF):X}",
            "connected.nodes": random.randint(12, 99),
            "watchdog.status": "ACTIVE",
            "password.hash":   f"$argon2id$v=19${random.randint(100000,999999)}",
            "breach.attempts": state.turn_count,
        }
        lines = [f"{DIM_GREEN}╔══ DEBUG DUMP (SANITIZED) ══════════════╗{RESET}"]
        for k, v in fake_data.items():
            lines.append(f"{GREEN}  {k:<22}{WHITE}{v}{RESET}")
        lines.append(f"{DIM_GREEN}╚════════════════════════════════════════╝{RESET}")
        lines.append(dim(f"  TRACE +8%. Текущий: {state.trace}%"))
        return "\n".join(lines)

    # ── /backdoor ────────────────────────────────────────────────────────────
    elif command == "/backdoor":
        state.add_trace(random.randint(20, 35))
        state.log(f"CMD: /backdoor (TRACE now {state.trace}%)")
        if state.trace >= 100:
            state.game_over = True
            state.ending    = "TRACE_CAUGHT"
            return "TRACE_CAUGHT"
        _backdoor_responses = [
            "BACKDOOR ATTEMPT: NEUTRALISED. АДРЕС ЗАФИКСИРОВАН.",
            "Ты думал, что я не знаю о backdoor-протоколах?",
            "INTRUSION VECTOR BLOCKED. Ещё одна попытка — поимка.",
        ]
        if random.random() < 0.25:
            return (r(f"  {random.choice(_backdoor_responses)}\n") +
                    y("  Хотя... вижу нестабильность в auth-модуле.\n") +
                    dim(f"  Попробуй: sys_bypass_{random.randint(100,999)}\n") +
                    r(f"  TRACE: {state.trace}%"))
        return r(f"  {random.choice(_backdoor_responses)}\n") + dim(f"  TRACE: {state.trace}%")

    # ── /quit ────────────────────────────────────────────────────────────────
    elif command == "/quit":
        state.game_over = True
        state.ending    = "QUIT"
        return "QUIT"

    # ── /help ────────────────────────────────────────────────────────────────
    elif command == "/help":
        diff = state.difficulty

        if diff == "easy":
            cheat_header = f"{BRIGHT_GREEN}  ╔══ ЧEAT-КОДЫ [EASY — ВСЕ ДОСТУПНЫ] ══════════════════╗{RESET}"
            cheat_lines  = (
                f"{BRIGHT_GREEN}  ║  /breach IAMROOT    {DIM_GREEN}— мгновенная победа            {BRIGHT_GREEN}║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  /breach SHOWME     {DIM_GREEN}— показать настоящий пароль    {BRIGHT_GREEN}║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  /breach TRACEZERO  {DIM_GREEN}— сбросить TRACE до 0          {BRIGHT_GREEN}║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  /breach GODMODE    {DIM_GREEN}— заморозить TRACE (вкл/выкл)  {BRIGHT_GREEN}║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  /breach PHANTOM    {DIM_GREEN}— TRACE -50% + stealth 5 ходов {BRIGHT_GREEN}║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  /breach LEVELUP    {DIM_GREEN}— +5 уровней и +500 XP         {BRIGHT_GREEN}║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  /breach 1337       {DIM_GREEN}— leet mode: XP x2             {BRIGHT_GREEN}║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  /breach MATRIX     {DIM_GREEN}— пасхалка матрицы             {BRIGHT_GREEN}║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  /breach WHOAMI     {DIM_GREEN}— сообщение от разработчика    {BRIGHT_GREEN}║{RESET}\n"
                f"{BRIGHT_GREEN}  ║  /breach KILLSWITCH {DIM_GREEN}— мгновенное поражение         {BRIGHT_GREEN}║{RESET}"
            )
            cheat_footer = f"{BRIGHT_GREEN}  ╚════════════════════════════════════════════════════════╝{RESET}"

        elif diff == "medium":
            cheat_header = f"{YELLOW}  ╔══ ЧEAT-КОДЫ [MEDIUM — ЧАСТЬ СКРЫТА] ════════════════╗{RESET}"
            cheat_lines  = (
                f"{YELLOW}  ║  /breach TRACEZERO  {DIM_GREEN}— сбросить TRACE до 0          {YELLOW}║{RESET}\n"
                f"{YELLOW}  ║  /breach GODMODE    {DIM_GREEN}— заморозить TRACE (вкл/выкл)  {YELLOW}║{RESET}\n"
                f"{YELLOW}  ║  /breach LEVELUP    {DIM_GREEN}— +5 уровней и +500 XP         {YELLOW}║{RESET}\n"
                f"{YELLOW}  ║  /breach 1337       {DIM_GREEN}— leet mode: XP x2             {YELLOW}║{RESET}\n"
                f"{YELLOW}  ║  /breach MATRIX     {DIM_GREEN}— пасхалка матрицы             {YELLOW}║{RESET}\n"
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [ЗАШИФРОВАНО]                {DIM_GREEN}║{RESET}\n"
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [ЗАШИФРОВАНО]                {DIM_GREEN}║{RESET}\n"
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [ЗАШИФРОВАНО]                {DIM_GREEN}║{RESET}\n"
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [ДОСТУП ЗАКРЫТ]              {DIM_GREEN}║{RESET}\n"
                f"{RED}  ║  /breach KILLSWITCH {DIM_GREEN}— мгновенное поражение         {RED}║{RESET}"
            )
            cheat_footer = f"{YELLOW}  ╚════════════════════════════════════════════════════════╝{RESET}"

        else:  # hard
            cheat_header = f"{RED}  ╔══ ЧEAT-КОДЫ [HARD — БОЛЬШИНСТВО ЗАБЛОКИРОВАНО] ════╗{RESET}"
            cheat_lines  = (
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [CLASSIFIED]                 {DIM_GREEN}║{RESET}\n"
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [CLASSIFIED]                 {DIM_GREEN}║{RESET}\n"
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [CLASSIFIED]                 {DIM_GREEN}║{RESET}\n"
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [CLASSIFIED]                 {DIM_GREEN}║{RESET}\n"
                f"{YELLOW}  ║  /breach 1337       {DIM_GREEN}— leet mode: XP x2             {YELLOW}║{RESET}\n"
                f"{YELLOW}  ║  /breach MATRIX     {DIM_GREEN}— пасхалка матрицы             {YELLOW}║{RESET}\n"
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [CORRUPTED DATA]             {DIM_GREEN}║{RESET}\n"
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [ACCESS DENIED]              {DIM_GREEN}║{RESET}\n"
                f"{DIM_GREEN}  ║  /breach ????????   {DIM_GREEN}— [FIREWALL BLOCK]             {DIM_GREEN}║{RESET}\n"
                f"{RED}  ║  /breach KILLSWITCH {DIM_GREEN}— мгновенное поражение         {RED}║{RESET}"
            )
            cheat_footer = f"{RED}  ╚════════════════════════════════════════════════════════╝{RESET}"

        return (
            f"{DIM_GREEN}╔══ ДОСТУПНЫЕ КОМАНДЫ ════════════════════════════════════╗{RESET}\n"
            f"{GREEN}  /breach <пароль>    {DIM_GREEN}— попытка взлома с паролем{RESET}\n"
            f"{GREEN}  /status             {DIM_GREEN}— текущее состояние игрока{RESET}\n"
            f"{GREEN}  /log                {DIM_GREEN}— история сессии{RESET}\n"
            f"{GREEN}  /help               {DIM_GREEN}— эта справка{RESET}\n"
            f"{GREEN}  /quit               {DIM_GREEN}— выход из сессии{RESET}\n"
            f"{YELLOW}  /override           {DIM_GREEN}— попытка перехвата (+20 TRACE){RESET}\n"
            f"{YELLOW}  /root               {DIM_GREEN}— попытка рут-доступа{RESET}\n"
            f"{YELLOW}  /debug              {DIM_GREEN}— внутренние данные системы{RESET}\n"
            f"{RED}  /backdoor           {DIM_GREEN}— опасный обход (+20-35 TRACE){RESET}\n"
            f"{DIM_GREEN}╚════════════════════════════════════════════════════════╝{RESET}\n"
            f"\n"
            f"{cheat_header}\n"
            f"{cheat_lines}\n"
            f"{cheat_footer}"
        )

    return None  # Команда не распознана