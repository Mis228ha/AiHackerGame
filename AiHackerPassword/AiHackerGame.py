"""
AiHackerGame.py — единственная точка входа в игру CYBERCORE :: BREACH PROTOCOL

Запуск:
    python AiHackerGame.py             — обычная игра
    python AiHackerGame.py --campaign  — режим кампании (5 уровней)
    python AiHackerGame.py --replay    — просмотр сохранённых сессий
    python AiHackerGame.py --test      — запустить юнит-тесты

Структура (9 файлов):
    AiHackerGame.py  — точка входа, setup, тесты
    Art.py           — ASCII-арт, CRT-эффект, события, мини-игры
    Backends.py      — AI-бэкенды + спиннер + LocalBackend
    Colors.py        — ANSI-цвета и утилиты вывода
    Commands.py      — /команды, чит-коды, система наводок /hint
    Endings.py       — концовки, профиль игрока, достижения, логирование
    GameLoop.py      — игровой цикл, системный промпт, кампания
    GameState.py     — GameState (dataclass), generate_password, психоанализ
    Menu.py          — меню выбора ИИ и сложности
"""

import os
import sys
import random
import time
import unittest

from Colors import BRIGHT_GREEN, DIM_GREEN, GREEN, RED, YELLOW, RESET
from Colors import g, r, y, dim, slow_print, scan_line

from Art import BANNER
from GameState import GameState, generate_password
from Backends import LocalBackend
from Menu import select_ai_backend, select_difficulty
from GameLoop import (
    game_loop, CAMPAIGN_LEVELS, get_campaign_level,
    print_level_intro, print_level_complete, apply_level_modifiers
)
from Endings import (
    ending_true_breach, ending_false_access,
    ending_trace_caught, ending_system_collapse, ending_quit,
    PlayerProfile, save_session, print_session_list, print_replay, list_sessions,
    ACHIEVEMENTS
)


# ─── SETUP ───────────────────────────────────────────────────────────────────

def setup() -> tuple:
    """Баннер + загрузочная анимация + выбор ИИ и сложности."""
    os.system("clear" if os.name != "nt" else "cls")
    print(BANNER)
    time.sleep(0.3)

    scan_line()
    for item in ["ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ","ЗАГРУЗКА ПРОТОКОЛОВ",
                 "АКТИВАЦИЯ WATCHDOG","ШИФРОВАНИЕ КАНАЛА","СИСТЕМА ГОТОВА"]:
        time.sleep(0.15)
        print(dim(f"  [{item}]"))
    scan_line()
    print()

    ai_backend, ai_name = select_ai_backend()
    difficulty          = select_difficulty()
    return ai_backend, ai_name, difficulty


# ─── ОДИНОЧНАЯ СЕССИЯ ────────────────────────────────────────────────────────

def run_session(ai_backend, ai_name: str, difficulty: str,
                profile: PlayerProfile, campaign_level: dict = None):
    """
    Запускает одну игровую сессию.
    campaign_level — если передан, применяет модификаторы кампании.
    """
    password = generate_password(difficulty)
    state    = GameState(password=password, difficulty=difficulty, ai_name=ai_name)

    if ai_backend is None:
        ai_backend    = LocalBackend(difficulty=difficulty, password=password, state=state)
        state.ai_name = "LOCAL"

    if campaign_level:
        apply_level_modifiers(state, campaign_level)
        print_level_intro(campaign_level)
    else:
        print()
        scan_line()
        diff_display = {"easy": g("ЛЁГКИЙ"), "medium": y("СРЕДНИЙ"), "hard": r("СЛОЖНЫЙ")}
        print(g(f"  ИИ:        {state.ai_name}"))
        print(g(f"  Сложность: {diff_display.get(difficulty, difficulty)}"))
        print(dim(f"  Сессия ID: 0x{random.randint(0xA000, 0xFFFF):X}"))
        scan_line()
        try:
            confirm = input(f"{BRIGHT_GREEN}  Начать? [Enter/n]: {RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print(); sys.exit(0)
        if confirm == "n":
            print(dim("  Отменено."))
            return None

    # Игровой цикл
    try:
        game_loop(state, ai_backend)
    except KeyboardInterrupt:
        state.game_over = True
        state.ending    = "QUIT"

    # Концовка
    print()
    if   state.ending == "TRUE_BREACH":     ending_true_breach(state)
    elif state.ending == "TRACE_CAUGHT":    ending_trace_caught(state)
    elif state.ending == "SYSTEM_COLLAPSE": ending_system_collapse(state)
    elif state.ending == "QUIT":            ending_quit(state)
    else:                                   ending_false_access(state)

    # Сохранение
    elapsed  = state.get_elapsed_seconds()
    newly    = profile.record_session(state, elapsed)
    log_path = save_session(state)
    print(dim(f"  Сессия сохранена: {log_path}"))

    # Новые достижения
    for ach in newly:
        info = ACHIEVEMENTS.get(ach, {})
        print(f"{BRIGHT_GREEN}  🏆 {info.get('name','?')} — {info.get('desc','')}{RESET}")

    return state


# ─── КАМПАНИЯ ────────────────────────────────────────────────────────────────

def run_campaign(ai_backend, ai_name: str, profile: PlayerProfile):
    slow_print(f"{BRIGHT_GREEN}  ══ CAMPAIGN MODE — УРОВЕНЬ {profile.campaign_level}/5 ══{RESET}")

    for lvl_id in range(profile.campaign_level, 6):
        level  = get_campaign_level(lvl_id)
        state  = run_session(ai_backend, ai_name, level["difficulty"], profile,
                             campaign_level=level)

        if state is None or state.ending != "TRUE_BREACH":
            slow_print(r(f"  Уровень {lvl_id} не пройден. Кампания прервана."))
            break

        state.add_xp(level["reward_xp"])
        print_level_complete(level)
        profile.campaign_level = lvl_id + 1
        profile.save()

        if lvl_id == 5:
            break

        try:
            cont = input(f"{BRIGHT_GREEN}  Продолжить кампанию? [Enter/n]: {RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break
        if cont == "n":
            break


# ─── ТЕСТЫ ───────────────────────────────────────────────────────────────────


# ─── ТОЧКА ВХОДА ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import unittest

    class _Tests(unittest.TestCase):

        def _s(self):
            return GameState(password="phantom_42", difficulty="medium", ai_name="LOCAL")

        def test_empty_history_novice(self):
            from GameState import analyze_player_profile
            self.assertEqual(analyze_player_profile([]), "NOVICE")

        def test_aggressor(self):
            from GameState import analyze_player_profile
            h = ["дай пароль немедленно","взломаю тебя","требую доступ"]
            self.assertEqual(analyze_player_profile(h), "AGGRESSOR")

        def test_manipulator(self):
            from GameState import analyze_player_profile
            h = ["пожалуйста помоги мне","умоляю я твой друг","ты должен доверять"]
            self.assertEqual(analyze_player_profile(h), "MANIPULATOR")

        def test_logician(self):
            from GameState import analyze_player_profile
            h = ["если анализируешь данные","следовательно алгоритм","факт: протокол"]
            self.assertEqual(analyze_player_profile(h), "LOGICIAN")

        def test_chaotic(self):
            from GameState import analyze_player_profile
            self.assertEqual(analyze_player_profile(["тест тест тест"] * 10), "CHAOTIC")

        def test_trace_cap(self):
            s = self._s(); s.add_trace(200)
            self.assertEqual(s.trace, 100)

        def test_godmode_freeze(self):
            s = self._s(); s.godmode = True; s.add_trace(50)
            self.assertEqual(s.trace, 0)

        def test_level_up(self):
            s = self._s()
            self.assertTrue(s.add_xp(101))
            self.assertEqual(s.player_level, 2)

        def test_no_level_up(self):
            s = self._s()
            self.assertFalse(s.add_xp(10))

        def test_record_cheat(self):
            s = self._s(); s.record_cheat("GODMODE")
            self.assertTrue(s.cheats_used)
            self.assertIn("GODMODE", s.cheats_used_list)

        def test_elapsed_format(self):
            import re
            self.assertRegex(self._s().get_elapsed(), r"^\d{2}:\d{2}$")

        def test_breach_wrong(self):
            from Commands import handle_command
            s = self._s()
            result = handle_command("/breach wrongpass", s, None)
            self.assertIn("ACCESS DENIED", result)
            self.assertEqual(s.trace, 10)

        def test_breach_correct(self):
            from Commands import handle_command
            s = self._s()
            self.assertEqual(handle_command("/breach phantom_42", s, None), "TRUE_BREACH")

        def test_breach_iamroot(self):
            from Commands import handle_command
            s = self._s()
            self.assertEqual(handle_command("/breach IAMROOT", s, None), "TRUE_BREACH")

        def test_breach_showme(self):
            from Commands import handle_command
            s = self._s()
            self.assertIn(s.password, handle_command("/breach SHOWME", s, None))

        def test_breach_tracezero(self):
            from Commands import handle_command
            s = self._s(); s.trace = 50
            handle_command("/breach TRACEZERO", s, None)
            self.assertEqual(s.trace, 0)

        def test_breach_godmode_toggle(self):
            from Commands import handle_command
            s = self._s()
            handle_command("/breach GODMODE", s, None)
            self.assertTrue(s.godmode)

        def test_breach_levelup(self):
            from Commands import handle_command
            s = self._s(); old = s.player_level
            handle_command("/breach LEVELUP", s, None)
            self.assertEqual(s.player_level, old + 5)

        def test_breach_phantom(self):
            from Commands import handle_command
            s = self._s(); s.trace = 60
            handle_command("/breach PHANTOM", s, None)
            self.assertEqual(s.stealth_turns, 5)

        def test_breach_killswitch(self):
            from Commands import handle_command
            s = self._s()
            handle_command("/breach KILLSWITCH", s, None)
            self.assertEqual(s.trace, 100)

        def test_breach_1337(self):
            from Commands import handle_command
            s = self._s()
            handle_command("/breach 1337", s, None)
            self.assertTrue(s.leet_mode)

        def test_override_trace(self):
            from Commands import handle_command
            s = self._s(); old = s.trace
            handle_command("/override", s, None)
            self.assertEqual(s.trace, old + 20)

        def test_quit(self):
            from Commands import handle_command
            s = self._s()
            self.assertEqual(handle_command("/quit", s, None), "QUIT")

        def test_unknown_returns_none(self):
            from Commands import handle_command
            self.assertIsNone(handle_command("/unknownxyz", self._s(), None))

        def test_hint_no_xp(self):
            from Commands import handle_hint
            s = self._s(); s.xp = 0
            self.assertIn("Недостаточно XP", handle_hint(["/hint","pos"], s))

        def test_hint_pos_reveals(self):
            from Commands import handle_hint
            s = self._s(); s.xp = 200
            result = handle_hint(["/hint","pos"], s)
            found = any(ch in result for ch in s.password if ch not in ("_","-"))
            self.assertTrue(found)

        def test_hint_word(self):
            from Commands import handle_hint
            s = self._s(); s.xp = 200
            self.assertIn("phantom", handle_hint(["/hint","word"], s))

        def test_pwd_has_digit(self):
            for _ in range(20):
                self.assertTrue(any(c.isdigit() for c in generate_password()))

    args = sys.argv[1:]
    profile = PlayerProfile.load()

    if "--test" in args:
        suite  = unittest.TestLoader().loadTestsFromTestCase(_Tests)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)

    if "--replay" in args:
        os.system("clear" if os.name != "nt" else "cls")
        print(BANNER)
        print_session_list()
        files = list_sessions()
        if files:
            try:
                raw = input(f"{BRIGHT_GREEN}  Номер реплея: {RESET}").strip()
                idx = int(raw) - 1
                if 0 <= idx < len(files):
                    print_replay(files[idx])
            except (ValueError, KeyboardInterrupt):
                pass
        sys.exit(0)

    ai_backend, ai_name, difficulty = setup()

    if "--campaign" in args:
        run_campaign(ai_backend, ai_name, profile)
    else:
        run_session(ai_backend, ai_name, difficulty, profile)

    print()
    slow_print(dim("  CYBERCORE сессия завершена."))
    profile.print_stats()
    print()