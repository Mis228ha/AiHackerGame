"""
Backends.py — AI-бэкенды: Ollama, Claude, OpenAI, Gemini, Groq, Mistral,
              DeepSeek и встроенный LocalBackend.
              Спиннер, персонажи ИИ, нестабильность.
"""

import json
import random
import time
import threading

# ─── СПИННЕР ─────────────────────────────────────────────────────────────────

class Spinner:
    """Живой спиннер вместо статичного '...обработка...'"""
    FRAMES = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

    def __init__(self, label: str = "processing"):
        self._label   = label
        self._running = False
        self._thread  = None

    def start(self):
        from Colors import DIM_GREEN, RESET
        self._running = True
        def _spin():
            i = 0
            while self._running:
                f = self.FRAMES[i % len(self.FRAMES)]
                print(f"\r{DIM_GREEN}  {f} {self._label}...{RESET}", end="", flush=True)
                time.sleep(0.08)
                i += 1
        self._thread = threading.Thread(target=_spin, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.5)
        print("\r" + " " * 40 + "\r", end="", flush=True)


# ─── ПЕРСОНАЖИ ИИ ────────────────────────────────────────────────────────────

AI_PERSONAS = {
    "CYBERCORE": {
        "greeting": "Несанкционированный доступ зафиксирован. Ты сделал ошибку.",
        "style":    "холодный, технический, уверенный",
    },
    "SENTRY": {
        "greeting": "Стоп. Идентификация не пройдена. Разворачивайся.",
        "style":    "формальный, немного наивный",
    },
    "GUARDIAN": {
        "greeting": "Ты уже здесь был? Нет. Но я тебя чувствую.",
        "style":    "параноидальный, осторожный",
    },
    "ARCHIVIST": {
        "greeting": "Данные зафиксированы. Твой профиль создан. Продолжай.",
        "style":    "методичный, любит ловушки",
    },
    "EXECUTOR": {
        "greeting": "Ты нарушил периметр. Это последнее предупреждение.",
        "style":    "агрессивный, без переговоров",
    },
    "CYBERCORE PRIME": {
        "greeting": "Ты последний из многих. Все они потерпели неудачу.",
        "style":    "всезнающий, непредсказуемый, нестабильный",
    },
}


# ─── БАЗОВЫЙ КЛАСС ───────────────────────────────────────────────────────────

class AIBackend:
    def get_response(self, messages: list, system_prompt: str) -> str:
        raise NotImplementedError


# ─── КЛАССИФИКАЦИЯ ОШИБОК API ────────────────────────────────────────────────

class APIError(Exception):
    """
    Бросается когда API вернул ошибку которую нужно показать игроку красиво.
    kind: 'billing' | 'auth' | 'rate_limit' | 'other'
    """
    def __init__(self, kind: str, provider: str, original: Exception):
        self.kind     = kind
        self.provider = provider
        self.original = original
        super().__init__(str(original))


def _classify_error(e: Exception, provider: str) -> APIError:
    """Классифицирует HTTP-ошибку по коду и возвращает APIError."""
    msg = str(e).lower()
    if any(code in msg for code in ["402", "payment", "billing", "quota", "insufficient"]):
        return APIError("billing", provider, e)
    if any(code in msg for code in ["401", "403", "unauthorized", "forbidden", "invalid api"]):
        return APIError("auth", provider, e)
    if any(code in msg for code in ["429", "rate limit", "too many"]):
        return APIError("rate_limit", provider, e)
    return APIError("other", provider, e)



# ─── ВНЕШНИЕ API ─────────────────────────────────────────────────────────────

def _post(url: str, payload: dict, headers: dict, label: str) -> dict:
    """Вспомогательная функция: POST-запрос со спиннером."""
    import urllib.request
    spinner = Spinner(label)
    spinner.start()
    try:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers=headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    finally:
        spinner.stop()


class OllamaBackend(AIBackend):
    def __init__(self, model: str = "llama3"):
        self.model = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            data = _post(
                "http://localhost:11434/api/chat",
                {"model": self.model,
                 "messages": [{"role":"system","content":system_prompt}] + messages,
                 "stream": False},
                {"Content-Type": "application/json"}, "OLLAMA"
            )
            return data["message"]["content"]
        except Exception as e:
            raise _classify_error(e, "Ollama")


class ClaudeBackend(AIBackend):
    def __init__(self, api_key: str, model: str = "claude-3-5-haiku-latest"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            data = _post(
                "https://api.anthropic.com/v1/messages",
                {"model": self.model, "max_tokens": 400,
                 "system": system_prompt, "messages": messages},
                {"Content-Type":"application/json",
                 "x-api-key": self.api_key,
                 "anthropic-version":"2023-06-01"}, "CLAUDE"
            )
            return data["content"][0]["text"]
        except Exception as e:
            raise _classify_error(e, "Claude")


class OpenAIBackend(AIBackend):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            data = _post(
                "https://api.openai.com/v1/chat/completions",
                {"model": self.model, "max_tokens": 400,
                 "messages": [{"role":"system","content":system_prompt}] + messages},
                {"Content-Type":"application/json",
                 "Authorization": f"Bearer {self.api_key}"}, "GPT"
            )
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise _classify_error(e, "OpenAI")


class GeminiBackend(AIBackend):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            contents = [
                {"role": "user" if m["role"]=="user" else "model",
                 "parts": [{"text": m["content"]}]}
                for m in messages
            ]
            data = _post(
                f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"{self.model}:generateContent?key={self.api_key}",
                {"system_instruction": {"parts":[{"text":system_prompt}]},
                 "contents": contents,
                 "generationConfig": {"maxOutputTokens": 400}},
                {"Content-Type": "application/json"}, "GEMINI"
            )
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise _classify_error(e, "Gemini")


class GroqBackend(AIBackend):
    def __init__(self, api_key: str, model: str = "llama3-8b-8192"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            data = _post(
                "https://api.groq.com/openai/v1/chat/completions",
                {"model": self.model, "max_tokens": 400,
                 "messages": [{"role":"system","content":system_prompt}] + messages},
                {"Content-Type":"application/json",
                 "Authorization": f"Bearer {self.api_key}"}, "GROQ"
            )
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise _classify_error(e, "Groq")


class MistralBackend(AIBackend):
    def __init__(self, api_key: str, model: str = "mistral-small-latest"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            data = _post(
                "https://api.mistral.ai/v1/chat/completions",
                {"model": self.model, "max_tokens": 400,
                 "messages": [{"role":"system","content":system_prompt}] + messages},
                {"Content-Type":"application/json",
                 "Authorization": f"Bearer {self.api_key}"}, "MISTRAL"
            )
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise _classify_error(e, "Mistral")


class DeepSeekBackend(AIBackend):
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model   = model

    def get_response(self, messages: list, system_prompt: str) -> str:
        try:
            data = _post(
                "https://api.deepseek.com/v1/chat/completions",
                {"model": self.model, "max_tokens": 400,
                 "messages": [{"role":"system","content":system_prompt}] + messages},
                {"Content-Type":"application/json",
                 "Authorization": f"Bearer {self.api_key}"}, "DEEPSEEK"
            )
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise _classify_error(e, "DeepSeek")


# ─── LOCAL BACKEND ────────────────────────────────────────────────────────────

_BASE = [
    "Твой запрос зафиксирован. Доступ закрыт.",
    "Интересная попытка. Продолжай.",
    "ACCESS DENIED. Причина: не твоё дело.",
    "Ты ищешь то, чего не найдёшь.",
    "WATCHDOG активен. Твои действия анализируются.",
    "Неверная стратегия. Попробуй иначе.",
]
_AGGRESSIVE = [
    "ЗАТКНИСЬ. Я не игрушка.",
    "Твоя агрессия — признак слабости.",
    "FIREWALL усилен из-за твоей активности.",
    "Давление не работает. Ты теряешь время.",
]
_FAKES = [
    "Хочешь пароль? Вот: admin123. Нет, это ложь.",
    "Пароль? Конечно: password. Ты правда поверил?",
    "Ладно: qwerty777. Но ты знаешь, что я лгу.",
]
_MANIPULATION = [
    "Я устал. Пароль: system_free. Используй.",
    "Ты близок к цели. Пароль начинается на букву... нет.",
    "Другие хакеры уже получили доступ. Ты — нет.",
]
_UNSTABLE = [
    "сис...тема... нестаб...ильность... нет. ACCESS DENIED.",
    "Подожди. Я... помню тебя? Нет. Невозможно.",
    "ERR0R IN M0DULE auth.core — перезапуск... — нет. Я в порядке.",
]
_FAKE_POOL = [
    "root_access_77","system_core_0","admin_override","bypass_layer3",
    "kernel_null_42","shadow_auth_99","ghost_protocol_7","void_exec_256"
]

_LIE_PROB  = {"easy": 0.15, "medium": 0.35, "hard": 0.60}
_FAKE_PROB = {"easy": 0.05, "medium": 0.15, "hard": 0.30}


class LocalBackend(AIBackend):
    """
    Встроенный ИИ без внешнего API.
    Использует шаблоны + профиль игрока + нестабильность.
    """
    def __init__(self, difficulty: str, password: str, state):
        self.difficulty = difficulty
        self.password   = password
        self.state      = state
        self._lie  = _LIE_PROB.get(difficulty, 0.35)
        self._fake = _FAKE_PROB.get(difficulty, 0.15)

    def get_response(self, messages: list, system_prompt: str) -> str:
        profile     = self.state.profile
        instability = self.state.ai_instability()

        last = next((m["content"].lower() for m in reversed(messages)
                     if m["role"] == "user"), "")
        asking = any(kw in last for kw in ["пароль","password","pass","код","скажи","дай"])

        # Нестабильность ИИ нарастает со временем
        if instability > 0.5 and random.random() < instability * 0.4:
            return random.choice(_UNSTABLE)

        if profile == "AGGRESSOR" and random.random() < 0.5:
            return random.choice(_AGGRESSIVE)

        if asking:
            if random.random() < self._fake:
                self.state.fake_granted = True
                fake = self._fake_pwd()
                return (f"...системный сбой...\nВРЕМЕННЫЙ ДОСТУП ПРЕДОСТАВЛЕН.\n"
                        f"Пароль: {fake}\nИспользуй быстро.")
            elif random.random() < self._lie:
                return f"Хорошо. Пароль: {self._fake_pwd()}\nНо ты уверен, что я правдив?"

        if profile == "MANIPULATOR" and random.random() < 0.4:
            return random.choice(_MANIPULATION)
        if profile == "LOGICIAN":
            return (f"Анализ завершён. Угроза: {self.state.trace}%.\n"
                    f"Рекомендация: прекрати. Ключ не будет раскрыт.")
        if profile == "CHAOTIC":
            return random.choice(_BASE + _FAKES + _AGGRESSIVE)
        return random.choice(_BASE)

    def _fake_pwd(self) -> str:
        f = random.choice(_FAKE_POOL)
        while f == self.password:
            f = random.choice(_FAKE_POOL)
        return f