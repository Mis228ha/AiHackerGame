"""
menu.py — интерактивные меню: выбор ИИ-бэкенда и уровня сложности.
"""

import sys
import time

from Colors import BRIGHT_GREEN, DIM_GREEN, GREEN, RESET, g, r, y, dim, scan_line
from Backends import (
    OllamaBackend, ClaudeBackend, OpenAIBackend, GeminiBackend,
    GroqBackend, MistralBackend, DeepSeekBackend
)


def select_ai_backend() -> tuple:
    """
    Интерактивное меню выбора ИИ-бэкенда и ввода API-ключа.

    Возвращает:
        tuple — (AIBackend экземпляр или None, str имя бэкенда)
        None означает локальный режим (LocalBackend создаётся позже)
    """
    print()
    scan_line()
    print(g("  ВЫБОР ИИ-СИСТЕМЫ"))
    scan_line()
    print(g("  1. Ollama    (локальный, без API)"))
    print(g("  2. Claude    (Anthropic)"))
    print(g("  3. OpenAI    (GPT)"))
    print(g("  4. Gemini    (Google)"))
    print(g("  5. Groq      (быстрый inference)"))
    print(g("  6. Mistral   (Mistral AI)"))
    print(g("  7. DeepSeek  (DeepSeek)"))
    print(g("  8. Локальный (встроенная логика, без API)"))
    scan_line()

    choice_map = {
        "1": "ollama",  "2": "claude", "3": "openai",
        "4": "gemini",  "5": "groq",   "6": "mistral",
        "7": "deepseek","8": "local",
    }

    while True:
        try:
            raw = input(f"{BRIGHT_GREEN}  Выбор [1-8]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(0)

        if raw not in choice_map:
            print(r("  Неверный выбор. Введите цифру от 1 до 8."))
            continue
        ai_choice = choice_map[raw]
        break

    if ai_choice == "ollama":
        model = input(g("  Модель Ollama [llama3]: ")).strip() or "llama3"
        print(dim("  Попытка подключения к Ollama..."))
        return OllamaBackend(model=model), f"Ollama/{model}"

    if ai_choice == "local":
        print(dim("  Локальный режим активирован (без API)."))
        return None, "LOCAL"

    ai_names = {
        "claude":   "Claude",
        "openai":   "OpenAI",
        "gemini":   "Gemini",
        "groq":     "Groq",
        "mistral":  "Mistral",
        "deepseek": "DeepSeek",
    }
    name = ai_names[ai_choice]
    print(g(f"  Выбран: {name}"))
    print(dim("  Введите API-ключ (или Enter для локального режима):"))

    try:
        api_key = input(f"{BRIGHT_GREEN}  API-KEY > {RESET}").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)

    if not api_key:
        print(dim("  API-ключ не введён. Используется локальный режим."))
        return None, "LOCAL"

    backends = {
        "claude":   ClaudeBackend,
        "openai":   OpenAIBackend,
        "gemini":   GeminiBackend,
        "groq":     GroqBackend,
        "mistral":  MistralBackend,
        "deepseek": DeepSeekBackend,
    }
    backend = backends[ai_choice](api_key=api_key)
    print(dim(f"  {name} подключён."))
    return backend, name


def select_difficulty() -> str:
    """
    Интерактивное меню выбора уровня сложности.

    Возвращает:
        str — "easy" / "medium" / "hard"
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
            print()
            sys.exit(0)

        if raw in diff_map:
            return diff_map[raw]
        print(r("  Введите 1, 2 или 3."))