"""
Menu.py — интерактивные меню: выбор ИИ-бэкенда и уровня сложности.
"""

import sys
from Colors import BRIGHT_GREEN, RESET, g, r, dim, scan_line
from Backends import (
    OllamaBackend, ClaudeBackend, OpenAIBackend, GeminiBackend,
    GroqBackend, MistralBackend, DeepSeekBackend
)


def select_ai_backend() -> tuple:
    """
    Меню выбора ИИ-бэкенда.
    Возвращает (AIBackend или None, str имя).
    None = локальный режим (LocalBackend создаётся позже в AiHackerGame).
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

    choices = {
        "1":"ollama","2":"claude","3":"openai","4":"gemini",
        "5":"groq","6":"mistral","7":"deepseek","8":"local"
    }
    while True:
        try:
            raw = input(f"{BRIGHT_GREEN}  Выбор [1-8]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(); sys.exit(0)
        if raw in choices:
            choice = choices[raw]
            break
        print(r("  Введите цифру от 1 до 8."))

    if choice == "ollama":
        model = input(g("  Модель Ollama [llama3]: ")).strip() or "llama3"
        return OllamaBackend(model=model), f"Ollama/{model}"

    if choice == "local":
        print(dim("  Локальный режим. API не нужен."))
        return None, "LOCAL"

    names = {
        "claude":"Claude","openai":"OpenAI","gemini":"Gemini",
        "groq":"Groq","mistral":"Mistral","deepseek":"DeepSeek"
    }
    name = names[choice]
    print(g(f"  Выбран: {name}"))
    print(dim("  API-ключ (или Enter → локальный режим):"))

    try:
        api_key = input(f"{BRIGHT_GREEN}  API-KEY > {RESET}").strip()
    except (KeyboardInterrupt, EOFError):
        print(); sys.exit(0)

    if not api_key:
        print(dim("  Ключ не введён. Локальный режим."))
        return None, "LOCAL"

    backends = {
        "claude":ClaudeBackend, "openai":OpenAIBackend, "gemini":GeminiBackend,
        "groq":GroqBackend, "mistral":MistralBackend, "deepseek":DeepSeekBackend
    }
    return backends[choice](api_key=api_key), name


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

    diff_map = {"1":"easy","2":"medium","3":"hard"}
    while True:
        try:
            raw = input(f"{BRIGHT_GREEN}  Выбор [1-3]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(); sys.exit(0)
        if raw in diff_map:
            return diff_map[raw]
        print(r("  Введите 1, 2 или 3."))