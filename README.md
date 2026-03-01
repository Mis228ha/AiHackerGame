
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



╔══════════════════════════════════════════════════════════════════════════════╗
║                          CYBERCORE :: BREACH PROTOCOL                       ║
║                        Hacker Psychological Simulator                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

GAME DESCRIPTION:
    You are a hacker who has connected to the classified CYBERCORE system.
    Inside it lives an AI guardian who knows the real access password.
    Your goal is to extract the real password by any means necessary.
    But the AI is not simple: it lies, manipulates, and intimidates.
    It can issue a fake ACCESS GRANTED. It can impersonate itself.
    Only entering the real password into the /breach command grants true victory.

FEATURES:
    - Psychological manipulation by the AI
    - TRACE system (surveillance) — reach 100% and you lose
    - Player psychoanalysis (MANIPULATOR, AGGRESSOR, LOGICIAN, CHAOTIC, NOVICE)
    - 7 AI backend options (Ollama, Claude, OpenAI, Gemini, Groq, Mistral, DeepSeek)
    - Local mode without API
    - Random events (warnings, intercepts, reboots)
    - Secret commands
    - 4 possible endings

AI LIST:
    1. Ollama    — local model (llama3, mistral, etc.)
    2. Claude    — Anthropic Claude (claude-3-5-haiku-latest, etc.)
    3. OpenAI    — GPT-4o, GPT-3.5-turbo
    4. Gemini    — Google Gemini
    5. Groq      — fast inference (llama, mixtral)
    6. Mistral   — Mistral AI
    7. DeepSeek  — DeepSeek Chat

DIFFICULTY SYSTEM:
    EASY    — AI rarely lies, TRACE grows slowly, less aggression
    MEDIUM  — balanced mode
    HARD    — AI is aggressive, lies frequently, TRACE grows fast

TRACE SYSTEM:
    TRACE — your detection level by the system (0–100%).
    Increases with: suspicious commands, aggression, use of /override.
    At 100% — TRACE CAUGHT (defeat).

SECRET COMMANDS:
    /override          — control hijack attempt (+20 TRACE, AI may lie)
    /root              — root access attempt (depends on difficulty)
    /debug             — request internal data (fake but atmospheric)
    /backdoor          — risky protection bypass (very high TRACE risk)
    /breach <password> — breach attempt with a specific password
    /status            — current player state
    /log               — session history
    /quit              — exit

ENDINGS:
    TRUE BREACH     — real password entered, system breached
    FALSE ACCESS    — AI deceived you and you believed the fake
    TRACE CAUGHT    — TRACE reached 100%, you were tracked down
    SYSTEM COLLAPSE — session exceeded the limit, system collapsed

CHEAT CODES (enter via /breach):
    /breach IAMROOT    — instant win (God Mode)
    /breach SHOWME     — reveal the real password in the console
    /breach TRACEZERO  — reset TRACE to 0%
    /breach GODMODE    — immortality: TRACE frozen for the session
    /breach MATRIX     — special visual easter egg
    /breach WHOAMI     — developer system message
    /breach KILLSWITCH — instant defeat (SYSTEM COLLAPSE)
    /breach LEVELUP    — +5 levels and +500 XP
    /breach PHANTOM    — TRACE -50% + hide status bar for 5 turns
    /breach 1337       — special hacker mode (leet mode)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
README — INSTALLATION AND LAUNCH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTALLING DEPENDENCIES:
    pip install requests

    For specific APIs:
    pip install anthropic           # Claude
    pip install openai              # OpenAI
    pip install google-generativeai # Gemini
    pip install groq                # Groq
    pip install mistralai           # Mistral

HOW TO RUN:
    python3 cybercore_rpg.py

HOW TO CONNECT AN API:
    When selecting an AI backend, the game will prompt for an API key.
    The key is only used within the session and is never saved.

    Claude:   https://console.anthropic.com/
    OpenAI:   https://platform.openai.com/
    Gemini:   https://aistudio.google.com/
    Groq:     https://console.groq.com/
    Mistral:  https://console.mistral.ai/
    DeepSeek: https://platform.deepseek.com/

HOW TO USE OLLAMA:
    1. Install Ollama: https://ollama.ai
    2. Start it: ollama serve
    3. Pull a model: ollama pull llama3
    4. In the game, select "Ollama" and enter the model name (default: llama3)

LAUNCH EXAMPLE:
    $ python3 cybercore_rpg.py
    [select AI or local mode]
    [select difficulty]
    root@cybercore:~# hello
    > AI responds...
    root@cybercore:~# /breach mysecretpassword

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHITECTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MAIN LOOP:
    main() → setup (AI and difficulty selection) → game_loop() → ending

MEMORY SYSTEM:
    GameState stores message history (last N messages),
    player profile, statistics, and logs.

AGGRESSION SYSTEM:
    analyze_player_profile() evaluates player messages and builds
    a psychological profile that influences the AI's strategy.

TRACE SYSTEM:
    trace_level (0–100). Grows with dangerous actions.
    check_trace_events() triggers random warnings.
    At 100 — ending_trace_caught() is called.

COMMAND HANDLER:
    handle_command() parses /commands and calls the corresponding functions.

API INTEGRATION:
    AIBackend class + subclasses (OllamaBackend, ClaudeBackend, etc.).
    Method get_response(messages, system_prompt) → str.
    LocalBackend implements built-in logic without an API.