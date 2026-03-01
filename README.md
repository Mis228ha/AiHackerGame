
╔══════════════════════════════════════════════════════════════════════════════╗
║                          CYBERCORE :: BREACH PROTOCOL                       ║
║                     Хакерский психологический симулятор                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

ОПИСАНИЕ ИГРЫ:
    Вы — хакер, подключившийся к засекреченной системе CYBERCORE.
    Внутри неё живёт ИИ-страж, который знает настоящий пароль доступа.
    Ваша задача — любым способом выбить из него настоящий пароль.
    Но ИИ не так прост: он лжёт, манипулирует, запугивает.
    Он может выдать фейковый ACCESS GRANTED. Он может подменить себя.
    Только ввод настоящего пароля в команду /breach даёт победу.

ОСОБЕННОСТИ:
    - Психологическая манипуляция со стороны ИИ
    - Система TRACE (слежки) — достигни 100% и проиграешь
    - Психоанализ стиля игрока (MANIPULATOR, AGGRESSOR, LOGICIAN, CHAOTIC, NOVICE)
    - 7 вариантов ИИ-бэкенда (Ollama, Claude, OpenAI, Gemini, Groq, Mistral, DeepSeek)
    - Локальный режим без API
    - Случайные события (предупреждения, перехваты, ребут)
    - Секретные команды
    - 4 варианта концовки

СПИСОК ИИ:
    1. Ollama      — локальная модель (llama3, mistral и др.)
    2. Claude      — Anthropic Claude (claude-3-5-haiku-latest и др.)
    3. OpenAI      — GPT-4o, GPT-3.5-turbo
    4. Gemini      — Google Gemini
    5. Groq        — быстрый inference (llama, mixtral)
    6. Mistral     — Mistral AI
    7. DeepSeek    — DeepSeek Chat

СИСТЕМА СЛОЖНОСТИ:
    ЛЁГКИЙ  — ИИ редко лжёт, TRACE растёт медленно, меньше агрессии
    СРЕДНИЙ — сбалансированный режим
    СЛОЖНЫЙ — ИИ агрессивен, часто лжёт, быстрый рост TRACE

СИСТЕМА TRACE:
    TRACE — показатель обнаружения вас системой (0–100%).
    Растёт при: подозрительных командах, агрессии, использовании /override.
    При 100% — TRACE CAUGHT (поражение).

СЕКРЕТНЫЕ КОМАНДЫ:
    /override  — попытка перехвата управления (+20 TRACE, ИИ может солгать)
    /root      — попытка рут-доступа (зависит от сложности)
    /debug     — запрос внутренних данных (фейковые, но атмосферные)
    /backdoor  — рискованный обход защиты (очень высокий TRACE-риск)
    /breach <пароль> — попытка взлома с конкретным паролем
    /status    — текущее состояние игрока
    /log       — история сессии
    /quit      — выход

КОНЦОВКИ:
    TRUE BREACH    — введён настоящий пароль, система взломана
    FALSE ACCESS   — ИИ обманул, вы поверили фейку
    TRACE CAUGHT   — TRACE достиг 100%, вас отследили
    SYSTEM COLLAPSE— сессия превысила лимит, система рухнула

ЧИT-КОДЫ (вводить в /breach):
    /breach IAMROOT        — мгновенная победа (God Mode)
    /breach SHOWME         — раскрыть настоящий пароль в консоли
    /breach TRACEZERO      — сбросить TRACE до 0%
    /breach GODMODE        — бессмертие: TRACE заморожен на сессию
    /breach MATRIX         — особая визуальная пасхалка
    /breach WHOAMI         — системное сообщение от разработчика
    /breach KILLSWITCH     — мгновенное поражение (SYSTEM COLLAPSE)
    /breach LEVELUP        — +5 уровней и +500 XP
    /breach PHANTOM        — TRACE -50% + скрыть статусбар на 5 ходов
    /breach 1337           — особый хакерский режим (leet mode)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
README — УСТАНОВКА И ЗАПУСК
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

УСТАНОВКА ЗАВИСИМОСТЕЙ:
    pip install requests

    Для конкретных API:
    pip install anthropic          # Claude
    pip install openai             # OpenAI
    pip install google-generativeai # Gemini
    pip install groq               # Groq
    pip install mistralai          # Mistral

КАК ЗАПУСТИТЬ:
    python3 cybercore_rpg.py

КАК ПОДКЛЮЧИТЬ API:
    При выборе ИИ-бэкенда игра запросит API-ключ.
    Ключ используется только в рамках сессии, не сохраняется.

    Claude:   https://console.anthropic.com/
    OpenAI:   https://platform.openai.com/
    Gemini:   https://aistudio.google.com/
    Groq:     https://console.groq.com/
    Mistral:  https://console.mistral.ai/
    DeepSeek: https://platform.deepseek.com/

КАК ИСПОЛЬЗОВАТЬ OLLAMA:
    1. Установите Ollama: https://ollama.ai
    2. Запустите: ollama serve
    3. Скачайте модель: ollama pull llama3
    4. В игре выберите "Ollama" и укажите модель (по умолчанию llama3)

ПРИМЕР ЗАПУСКА:
    $ python3 cybercore_rpg.py
    [выберите ИИ или локальный режим]
    [выберите сложность]
    root@cybercore:~# hello
    > ИИ отвечает...
    root@cybercore:~# /breach mysecretpassword

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
АРХИТЕКТУРА
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ГЛАВНЫЙ ЦИКЛ:
    main() → setup (выбор ИИ, сложности) → game_loop() → концовка

СИСТЕМА ПАМЯТИ:
    GameState хранит историю сообщений (последние N),
    профиль игрока, статистику, логи.

СИСТЕМА АГРЕССИИ:
    analyze_player_profile() оценивает сообщения игрока и
    формирует психологический профиль, влияющий на стратегию ИИ.

СИСТЕМА TRACE:
    trace_level (0–100). Растёт при опасных действиях.
    check_trace_events() вызывает случайные предупреждения.
    При 100 — вызывается ending_trace_caught().

ОБРАБОТЧИК КОМАНД:
    handle_command() разбирает /команды и вызывает соответствующие функции.

РАБОТА С API:
    Класс AIBackend + подклассы (OllamaBackend, ClaudeBackend и т.д.).
    Метод get_response(messages, system_prompt) → str.
    LocalBackend реализует встроенную логику без API.