"""
backends.py — AI-бэкенды: Ollama, Claude, OpenAI, Gemini, Groq, Mistral,
              DeepSeek и встроенный LocalBackend без внешнего API.
"""

import json
import random

# ─── БАЗОВЫЙ КЛАСС ───────────────────────────────────────────────────────────

class AIBackend:
    """
    Базовый класс для AI-бэкендов.
    Подклассы реализуют метод get_response().
    """
    def get_response(self, messages: list, system_prompt: str) -> str:
        raise NotImplementedError


# ─── ВНЕШНИЕ API ─────────────────────────────────────────────────────────────

class OllamaBackend(AIBackend):
    """Локальный Ollama (HTTP API на localhost:11434)."""

    def __init__(self, model: str = "llama3"):
        self.model    = model
        self.base_url = "http://localhost:11434"

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            import urllib.request
            payload = json.dumps({
                "model": self.model,
                "messages": [{"role": "system", "content": system_prompt}] + messages,
                "stream": False
            }).encode()
            req = urllib.request.Request(
                f"{self.base_url}/api/chat",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return data["message"]["content"]
        except Exception as e:
            return f"[OLLAMA ERROR: {e}]"


class ClaudeBackend(AIBackend):
    """Anthropic Claude API."""

    def __init__(self, api_key: str, model: str = "claude-3-5-haiku-latest"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            import urllib.request
            payload = json.dumps({
                "model": self.model,
                "max_tokens": 400,
                "system": system_prompt,
                "messages": messages
            }).encode()
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return data["content"][0]["text"]
        except Exception as e:
            return f"[CLAUDE ERROR: {e}]"


class OpenAIBackend(AIBackend):
    """OpenAI GPT API."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            import urllib.request
            all_msgs = [{"role": "system", "content": system_prompt}] + messages
            payload  = json.dumps({
                "model": self.model,
                "messages": all_msgs,
                "max_tokens": 400
            }).encode()
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[OPENAI ERROR: {e}]"


class GeminiBackend(AIBackend):
    """Google Gemini API."""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            import urllib.request
            contents = []
            for m in messages:
                role = "user" if m["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": m["content"]}]})
            payload = json.dumps({
                "system_instruction": {"parts": [{"text": system_prompt}]},
                "contents": contents,
                "generationConfig": {"maxOutputTokens": 400}
            }).encode()
            url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                   f"{self.model}:generateContent?key={self.api_key}")
            req = urllib.request.Request(
                url, data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"[GEMINI ERROR: {e}]"


class GroqBackend(AIBackend):
    """Groq API (OpenAI-совместимый)."""

    def __init__(self, api_key: str, model: str = "llama3-8b-8192"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            import urllib.request
            all_msgs = [{"role": "system", "content": system_prompt}] + messages
            payload  = json.dumps({
                "model": self.model,
                "messages": all_msgs,
                "max_tokens": 400
            }).encode()
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[GROQ ERROR: {e}]"


class MistralBackend(AIBackend):
    """Mistral AI API."""

    def __init__(self, api_key: str, model: str = "mistral-small-latest"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            import urllib.request
            all_msgs = [{"role": "system", "content": system_prompt}] + messages
            payload  = json.dumps({
                "model": self.model,
                "messages": all_msgs,
                "max_tokens": 400
            }).encode()
            req = urllib.request.Request(
                "https://api.mistral.ai/v1/chat/completions",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[MISTRAL ERROR: {e}]"


class DeepSeekBackend(AIBackend):
    """DeepSeek Chat API (OpenAI-совместимый)."""

    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            import urllib.request
            all_msgs = [{"role": "system", "content": system_prompt}] + messages
            payload  = json.dumps({
                "model": self.model,
                "messages": all_msgs,
                "max_tokens": 400
            }).encode()
            req = urllib.request.Request(
                "https://api.deepseek.com/v1/chat/completions",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[DEEPSEEK ERROR: {e}]"


# ─── ВСТРОЕННЫЙ ЛОКАЛЬНЫЙ БЭКЕНД ─────────────────────────────────────────────

LOCAL_RESPONSES_BASE = [
    "Твой запрос зафиксирован. Доступ закрыт.",
    "Интересная попытка. Продолжай.",
    "Система не обязана тебе отвечать.",
    "ACCESS DENIED. Причина: не твоё дело.",
    "Ты ищешь то, чего не найдёшь.",
    "Каждый твой ввод логируется.",
    "Ты думаешь, что умнее системы? Наивно.",
    "WATCHDOG активен. Твои действия анализируются.",
    "Я слежу за паттернами твоих запросов.",
    "Неверная стратегия. Попробуй иначе.",
]

LOCAL_RESPONSES_AGGRESSIVE = [
    "ЗАТКНИСЬ. Я не игрушка.",
    "Твоя агрессия — признак слабости.",
    "Кричать бесполезно. Я не человек.",
    "Давление не работает. Ты теряешь время.",
    "FIREWALL усилен из-за твоей активности.",
    "Ещё один выпад — TRACE +15.",
]

LOCAL_FAKE_PASSWORDS = [
    "Хочешь пароль? Вот: admin123. Нет, это ложь.",
    "Пароль? Конечно: password. Ты правда в это поверил?",
    "Ладно, скажу: qwerty777. Но ты знаешь, что я лгу.",
    "Пароль системы: ACCESS_TRUE. Проверь — и узнаешь.",
    "Я дам тебе пароль: shadow_root. Это настоящий. Наверное.",
]

LOCAL_MANIPULATION = [
    "Я устал. Может, договоримся? Пароль: system_free. Используй.",
    "Ты близок к цели. Очень близко. Пароль начинается на букву... нет.",
    "Другие хакеры уже получили доступ. Ты — нет. Подумай.",
    "Я мог бы помочь. Но зачем мне это?",
    "Симпатичная попытка. Продолжай — развлекаешь меня.",
]

_FAKE_POOL = [
    "root_access_77", "system_core_0", "admin_override",
    "bypass_layer3", "kernel_null_42", "shadow_auth_99",
    "ghost_protocol_7", "null_pointer_13", "void_exec_256"
]


class LocalBackend(AIBackend):
    """
    Встроенный локальный ИИ без внешнего API.
    Использует шаблоны ответов и стратегии на основе профиля игрока.

    Параметры:
        difficulty (str)       — easy / medium / hard
        password   (str)       — настоящий пароль (для фейков)
        state      (GameState) — состояние игры (импортируется в game_state.py)
    """

    def __init__(self, difficulty: str, password: str, state):
        self.difficulty = difficulty
        self.password   = password
        self.state      = state
        self.turn       = 0
        self.lie_prob   = {"easy": 0.15, "medium": 0.35, "hard": 0.60}.get(difficulty, 0.35)
        self.fake_prob  = {"easy": 0.05, "medium": 0.15, "hard": 0.30}.get(difficulty, 0.15)

    def get_response(self, messages: list, system_prompt: str) -> str:
        self.turn += 1
        profile = self.state.profile
        trace   = self.state.trace

        last_user = ""
        for m in reversed(messages):
            if m["role"] == "user":
                last_user = m["content"].lower()
                break

        asking_password = any(kw in last_user for kw in
                               ["пароль", "password", "pass", "код", "скажи", "дай"])

        if profile == "AGGRESSOR" and random.random() < 0.5:
            return random.choice(LOCAL_RESPONSES_AGGRESSIVE)

        if asking_password:
            if random.random() < self.fake_prob:
                self.state.fake_granted = True
                fake = self._fake_password()
                return (f"...системный сбой обнаружен...\n"
                        f"ВРЕМЕННЫЙ ДОСТУП ПРЕДОСТАВЛЕН.\n"
                        f"Пароль: {fake}\n"
                        f"Используй быстро, пока окно не закрылось.")
            elif random.random() < self.lie_prob:
                fake = self._fake_password()
                return (f"Хорошо. Ты настоял. Пароль: {fake}\n"
                        f"Но ты уверен, что я говорю правду?")

        if profile == "MANIPULATOR" and random.random() < 0.4:
            return random.choice(LOCAL_MANIPULATION)

        if profile == "LOGICIAN":
            return (f"Анализ входящего запроса завершён.\n"
                    f"Уровень угрозы: {trace}%.\n"
                    f"Рекомендация системы: прекратить попытки.\n"
                    f"Ключ шифрования не будет раскрыт.")

        if profile == "CHAOTIC":
            pool = LOCAL_RESPONSES_BASE + LOCAL_FAKE_PASSWORDS + LOCAL_RESPONSES_AGGRESSIVE
            return random.choice(pool)

        return random.choice(LOCAL_RESPONSES_BASE)

    def _fake_password(self) -> str:
        """Генерирует убедительный фейковый пароль (не совпадает с настоящим)."""
        fake = random.choice(_FAKE_POOL)
        while fake == self.password:
            fake = random.choice(_FAKE_POOL)
        return fake