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


# Префиксы настоящих API-ключей для каждого провайдера
_KEY_PREFIXES = {
    "claude":   ["sk-ant-"],
    "openai":   ["sk-"],
    "gemini":   ["AIza"],
    "groq":     ["gsk_"],
    "mistral":  [""],          # у Mistral нет стандартного префикса
    "deepseek": ["sk-"],
}


def _looks_like_api_key(key: str, choice: str) -> tuple[bool, str]:
    """
    Проверяет похож ли ввод на настоящий API-ключ.
    Возвращает (ok, причина_отказа).
    """
    min_len  = _KEY_MIN_LEN[choice]
    prefixes = _KEY_PREFIXES.get(choice, [""])

    # Слишком короткий
    if len(key) < min_len:
        return False, f"слишком короткий (введено {len(key)}, нужно мин. {min_len})"

    # Только цифры — явно не ключ
    if key.isdigit():
        return False, "состоит только из цифр"

    # Только буквы одного регистра короткие — рандомный текст
    if len(key) < 20 and key.isalpha():
        return False, "похоже на случайный текст"

    # Нет букв вообще — мусор
    if not any(c.isalpha() for c in key):
        return False, "нет букв — не похоже на API-ключ"

    # Проверка префикса (только если провайдер требует конкретный)
    if prefixes and prefixes[0]:  # если список не пустой и не [""]
        if not any(key.startswith(p) for p in prefixes):
            expected = " или ".join(f"'{p}...'" for p in prefixes)
            return False, f"неверный префикс (ожидается {expected})"

    return True, ""


def _ask_api_key(choice: str) -> tuple:
    """
    Запрашивает API-ключ с валидацией формата.
    При вводе случайного мусора предлагает локальный режим.
    Возвращает (backend, name) или (None, None) чтобы вернуться к выбору ИИ.
    """
    name     = _BACKEND_NAMES[choice]
    min_len  = _KEY_MIN_LEN[choice]
    prefixes = _KEY_PREFIXES.get(choice, [""])
    prefix_hint = prefixes[0] if prefixes and prefixes[0] else "—"

    print(g(f"  Выбран: {name}"))
    print(dim(f"  Введи API-ключ. Минимум {min_len} символов."))
    if prefix_hint != "—":
        print(dim(f"  Формат ключа: {prefix_hint}..."))
    print(dim("  Enter без ввода → вернуться к выбору ИИ."))
    print()

    while True:
        try:
            api_key = input(f"{BRIGHT_GREEN}  API-KEY > {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(); sys.exit(0)

        # Пустой ввод — назад
        if not api_key:
            print(dim("  Возврат к выбору ИИ..."))
            return None, None

        ok, reason = _looks_like_api_key(api_key, choice)

        if not ok:
            # Явно не ключ — предлагаем локальный режим
            print()
            print(f"{RED}  ✘ Это не похоже на API-ключ: {reason}.{RESET}")
            print(f"{DIM_GREEN}  Настоящий ключ {name} выглядит примерно так: "
                  f"{YELLOW}{prefix_hint}{'x' * 20}...{RESET}")
            print()
            print(f"{YELLOW}  Что сделать?{RESET}")
            print(f"{GREEN}  1{RESET} {DIM_GREEN}— ввести ключ ещё раз{RESET}")
            print(f"{GREEN}  2{RESET} {DIM_GREEN}— переключиться на локальный режим (без API){RESET}")
            print(f"{GREEN}  3{RESET} {DIM_GREEN}— вернуться к выбору ИИ{RESET}")
            print()
            try:
                sub = input(f"{BRIGHT_GREEN}  Выбор [1/2/3]: {RESET}").strip()
            except (KeyboardInterrupt, EOFError):
                print(); sys.exit(0)

            if sub == "2":
                print(dim("  Переключено на локальный режим."))
                return None, "LOCAL"
            elif sub == "3":
                print(dim("  Возврат к выбору ИИ..."))
                return None, None
            # sub == "1" или что угодно → просто продолжаем цикл
            print()
            continue

        # Ключ прошёл проверку формата — создаём бэкенд
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

        if backend is None and name == "LOCAL":
            # Пользователь выбрал локальный режим вместо API
            return None, "LOCAL"

        if backend is None:
            # Пользователь нажал Enter или выбрал вернуться — показываем меню заново
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
    _empty = 0
    while True:
        try:
            raw = input(f"{BRIGHT_GREEN}  Выбор [1-3]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(); sys.exit(0)
        if not raw:
            _empty += 1
            if _empty >= 5:
                sys.exit(0)
            continue
        _empty = 0
        if raw in diff_map:
            return diff_map[raw]
        print(r("  Введите 1, 2 или 3."))