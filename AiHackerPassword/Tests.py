"""
Tests.py — юнит-тесты для CYBERCORE :: BREACH PROTOCOL

Запуск:
    python Tests.py
    python Tests.py -v
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from GameState import GameState, generate_password, analyze_player_profile
from Commands import handle_command, handle_hint


class TestProfile(unittest.TestCase):

    def test_empty_novice(self):
        self.assertEqual(analyze_player_profile([]), "NOVICE")

    def test_aggressor(self):
        h = ["дай пароль немедленно", "взломаю тебя", "требую доступ"]
        self.assertEqual(analyze_player_profile(h), "AGGRESSOR")

    def test_manipulator(self):
        h = ["пожалуйста помоги мне", "умоляю я твой друг", "ты должен доверять"]
        self.assertEqual(analyze_player_profile(h), "MANIPULATOR")

    def test_logician(self):
        h = ["если анализируешь данные", "следовательно алгоритм", "факт: протокол"]
        self.assertEqual(analyze_player_profile(h), "LOGICIAN")

    def test_chaotic(self):
        self.assertEqual(analyze_player_profile(["тест тест тест"] * 10), "CHAOTIC")


class TestGameState(unittest.TestCase):

    def _s(self):
        return GameState(password="phantom_42", difficulty="medium", ai_name="LOCAL")

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

    def test_cheat_no_dupes(self):
        s = self._s(); s.record_cheat("X"); s.record_cheat("X")
        self.assertEqual(s.cheats_used_list.count("X"), 1)

    def test_elapsed_format(self):
        import re
        self.assertRegex(self._s().get_elapsed(), r"^\d{2}:\d{2}$")


class TestCommands(unittest.TestCase):

    def _s(self):
        return GameState(password="phantom_42", difficulty="medium", ai_name="LOCAL")

    def test_breach_wrong(self):
        s = self._s()
        result = handle_command("/breach wrongpass", s, None)
        self.assertIn("ACCESS DENIED", result)
        self.assertEqual(s.trace, 10)

    def test_breach_correct(self):
        s = self._s()
        self.assertEqual(handle_command("/breach phantom_42", s, None), "TRUE_BREACH")
        self.assertTrue(s.game_over)

    def test_breach_iamroot(self):
        s = self._s()
        self.assertEqual(handle_command("/breach IAMROOT", s, None), "TRUE_BREACH")

    def test_breach_showme(self):
        s = self._s()
        self.assertIn(s.password, handle_command("/breach SHOWME", s, None))

    def test_breach_tracezero(self):
        s = self._s(); s.trace = 50
        handle_command("/breach TRACEZERO", s, None)
        self.assertEqual(s.trace, 0)

    def test_breach_godmode(self):
        s = self._s()
        handle_command("/breach GODMODE", s, None)
        self.assertTrue(s.godmode)

    def test_breach_levelup(self):
        s = self._s(); old = s.player_level
        handle_command("/breach LEVELUP", s, None)
        self.assertEqual(s.player_level, old + 5)

    def test_breach_phantom(self):
        s = self._s(); s.trace = 60
        handle_command("/breach PHANTOM", s, None)
        self.assertEqual(s.stealth_turns, 5)

    def test_breach_killswitch(self):
        s = self._s()
        handle_command("/breach KILLSWITCH", s, None)
        self.assertEqual(s.trace, 100)

    def test_breach_1337(self):
        s = self._s()
        handle_command("/breach 1337", s, None)
        self.assertTrue(s.leet_mode)

    def test_override_trace(self):
        s = self._s(); old = s.trace
        handle_command("/override", s, None)
        self.assertEqual(s.trace, old + 20)

    def test_quit(self):
        s = self._s()
        self.assertEqual(handle_command("/quit", s, None), "QUIT")
        self.assertTrue(s.game_over)

    def test_unknown_returns_none(self):
        self.assertIsNone(handle_command("/unknownxyz", self._s(), None))

    def test_debug_trace(self):
        s = self._s(); old = s.trace
        handle_command("/debug", s, None)
        self.assertEqual(s.trace, old + 8)


class TestHints(unittest.TestCase):

    def _s(self, xp=200):
        s = GameState(password="phantom_42", difficulty="medium", ai_name="LOCAL")
        s.xp = xp
        return s

    def test_no_xp(self):
        self.assertIn("Недостаточно XP", handle_hint(["/hint", "pos"], self._s(xp=0)))

    def test_pos_reveals_char(self):
        s = self._s()
        result = handle_hint(["/hint", "pos"], s)
        found = any(ch in result for ch in s.password if ch not in ("_", "-"))
        self.assertTrue(found)

    def test_excl(self):
        self.assertIn("ENTROPY", handle_hint(["/hint", "excl"], self._s()))

    def test_word(self):
        self.assertIn("phantom", handle_hint(["/hint", "word"], self._s()))


class TestPassword(unittest.TestCase):

    def test_has_digit(self):
        for _ in range(20):
            self.assertTrue(any(c.isdigit() for c in generate_password()))

    def test_hard_uses_hard_words(self):
        hard = {"synapse","lattice","fractal","entropy","quantum",
                "chimera","oblivion","axiom","tachyon","paradox"}
        found = any(
            "".join(c for c in generate_password("hard") if c.isalpha()) in hard
            for _ in range(50)
        )
        self.assertTrue(found)


if __name__ == "__main__":
    verbosity = 2 if "-v" in sys.argv else 1
    unittest.main(verbosity=verbosity)