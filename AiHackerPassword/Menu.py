"""
Menu.py — интерактивные меню: выбор ИИ-бэкенда и уровня сложности.
"""

import sys
from Colors import BRIGHT_GREEN, GREEN, DIM_GREEN, YELLOW, RED, RESET, g, r, y, dim, scan_line
from Backends import (
    OllamaBackend, ClaudeBackend, OpenAIBackend, GeminiBackend,
    GroqBackend, MistralBackend, DeepSeekBackend
)

# Минимальные длины ключей для каждого провайдера (грубая проверка формата)
_KEY_MIN_LEN = {
    "claude":   40,   # sk-ant-...
    "openai":   40,   # sk-...
    "gemini":   30,
    "groq":     40,
    "mistral":  30,
    "deepseek": 30,
}

_BACKEND_NAMES = {
    "claude":   "Claude",
    "openai":   "OpenAI",
    "gemini":   "Gemini",
    "groq":     "Groq",
    "mistral":  "Mistral",
    "deepseek": "DeepSeek",
}

_BACKENDS = {
    "claude":   ClaudeBackend,
    "openai":   OpenAIBackend,
    "gemini":   GeminiBackend,
    "groq":     GroqBackend,
    "mistral":  MistralBackend,
    "deepseek": DeepSeekBackend,
}


def _print_ai_menu():
    print()
    scan_line()
    print(g("  ВЫБОР ИИ-СИСТЕМЫ"))
    scan_line()
    print(g("  1. Ollama    ") + dim("(локальный, без API)"))
    print(g("  2. Claude    ") + dim("(Anthropic)"))
    print(g("  3. OpenAI    ") + dim("(GPT)"))
    print(g("  4. Gemini    ") + dim("(Google)"))
    print(g("  5. Groq      ") + dim("(быстрый inference)"))
    print(g("  6. Mistral   ") + dim("(Mistral AI)"))
    print(g("  7. DeepSeek  ") + dim("(DeepSeek)"))
    print(g("  8. Локальный ") + dim("(встроенная логика, без API)"))
    scan_line()


def _ask_api_key(choice: str) -> tuple:
    """
    Запрашивает API-ключ с валидацией.
    Возвращает (backend, name) или (None, None) если нужно вернуться к выбору ИИ.
    """
    name    = _BACKEND_NAMES[choice]
    min_len = _KEY_MIN_LEN[choice]

    print(g(f"  Выбран: {name}"))
    print(dim(f"  Введи API-ключ (мин. {min_len} символов)."))
    print(dim("  Enter без ввода → вернуться к выбору ИИ."))
    print()

    attempts = 0
    while True:
        try:
            api_key = input(f"{BRIGHT_GREEN}  API-KEY > {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(); sys.exit(0)

        # Пустой ввод — вернуться назад
        if not api_key:
            print(dim("  Возврат к выбору ИИ..."))
            return None, None

        # Слишком короткий или явно не ключ (нет цифробукв)
        has_alnum = any(c.isalnum() for c in api_key)
        if len(api_key) < min_len or not has_alnum:
            attempts += 1
            print(r(f"  Ключ выглядит некорректно (слишком короткий или неверный формат)."))
            if attempts >= 2:
                print(y("  Подсказка: ключи обычно выглядят как 'sk-ant-api...' или 'AIzaSy...'"))
                print(y("  Нажми Enter без ввода чтобы выбрать другой ИИ или локальный режим."))
            continue

        # Ключ выглядит OK — создаём бэкенд
        return _BACKENDS[choice](api_key=api_key), name


def select_ai_backend() -> tuple:
    """
    Меню выбора ИИ-бэкенда с валидацией API-ключа.
    При некорректном ключе возвращает игрока обратно к выбору ИИ.
    Возвращает (AIBackend или None, str имя).
    None = локальный режим (LocalBackend создаётся в AiHackerGame).
    """
    choices = {
        "1": "ollama", "2": "claude", "3": "openai", "4": "gemini",
        "5": "groq",   "6": "mistral","7": "deepseek","8": "local"
    }

    while True:
        _print_ai_menu()

        while True:
            try:
                raw = input(f"{BRIGHT_GREEN}  Выбор [1-8]: {RESET}").strip()
            except (KeyboardInterrupt, EOFError):
                print(); sys.exit(0)
            if raw in choices:
                choice = choices[raw]
                break
            print(r("  Введите цифру от 1 до 8."))

        # ── Ollama ───────────────────────────────────────────────────────────
        if choice == "ollama":
            try:
                model = input(g("  Модель Ollama [llama3]: ")).strip() or "llama3"
            except (KeyboardInterrupt, EOFError):
                print(); sys.exit(0)
            return OllamaBackend(model=model), f"Ollama/{model}"

        # ── Локальный ────────────────────────────────────────────────────────
        if choice == "local":
            print(dim("  Локальный режим. API не нужен."))
            return None, "LOCAL"

        # ── API-бэкенды: запрашиваем ключ ────────────────────────────────────
        backend, name = _ask_api_key(choice)

        if backend is None:
            # Пользователь нажал Enter без ввода — показываем меню заново
            print()
            print(y("  Выбери другой ИИ или выбери '8' для локального режима (без API)."))
            continue

        return backend, name


def select_difficulty() -> str:
    """
    Меню выбора уровня сложности.
    Возвращает: "easy" | "medium" | "hard"
    """
    print()
    scan_line()
    print(g("  УРОВЕНЬ СЛОЖНОСТИ"))
    scan_line()
    print(g("  1. ЛЁГКИЙ  ") + dim("— ИИ редко лжёт, TRACE медленный"))
    print(g("  2. СРЕДНИЙ ") + dim("— сбалансированный режим"))
    print(g("  3. СЛОЖНЫЙ ") + r("— ИИ агрессивен, TRACE быстрый"))
    scan_line()

    diff_map = {"1": "easy", "2": "medium", "3": "hard"}
    while True:
        try:
            raw = input(f"{BRIGHT_GREEN}  Выбор [1-3]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(); sys.exit(0)
        if raw in diff_map:
            return diff_map[raw]
        print(r("  Введите 1, 2 или 3."))