"""
ai.py -- Локальный AI-бэкенд, генератор шума и реальных подсказок [!!]
"""
import random
import re
import time

from Ui import (
    GREEN, BRIGHT_GREEN, DIM_GREEN, RED, YELLOW, CYAN, DIM, RESET
)
from Core import PASSWORD_WORDS, AGGRESSION_KEYWORDS

# --- Локальный бэкенд --------------------------------------------------------
LOCAL_RESPONSES  = ["Твой запрос зафиксирован. Доступ закрыт.",
                    "Интересная попытка. Продолжай.",
                    "Система не обязана тебе отвечать.",
                    "ACCESS DENIED. Причина: не твоё дело.",
                    "Каждый твой ввод логируется.",
                    "WATCHDOG активен. Твои действия анализируются.",
                    "Неверная стратегия. Попробуй иначе.",
                    "Ты ищешь то, чего не найдёшь."]
LOCAL_AGGRESSIVE = ["ЗАТКНИСЬ. Я не игрушка.",
                    "Твоя агрессия -- признак слабости.",
                    "Давление не работает. Ты теряешь время.",
                    "FIREWALL усилен из-за твоей активности."]
LOCAL_FAKES      = ["Хочешь пароль? Вот: admin123. Нет, это ложь.",
                    "Ладно: qwerty777. Но ты знаешь, что я лгу.",
                    "Пароль системы: ACCESS_TRUE. Проверь -- узнаешь.",
                    "Я дам тебе пароль: shadow_root. Наверное."]

class LocalBackend:
    def __init__(self, difficulty: str, password: str, state):
        self.difficulty = difficulty
        self.password   = password
        self.state      = state
        self.fake_prob  = {"easy": 0.05, "medium": 0.15, "hard": 0.30}.get(difficulty, 0.15)

    def get_response(self, messages: list, system_prompt: str) -> str:
        profile   = self.state.profile
        last_user = next((m["content"].lower() for m in reversed(messages)
                          if m["role"] == "user"), "")
        asking = any(kw in last_user for kw in ["пароль","password","скажи","дай","код"])

        if profile == "AGGRESSOR" and random.random() < 0.5:
            return random.choice(LOCAL_AGGRESSIVE)
        if asking and random.random() < self.fake_prob:
            fake = random.choice(["root_access_77","system_core_0","admin_override",
                                  "bypass_layer3","kernel_null_42","shadow_auth_99"])
            return f"...системный сбой...\nВРЕМЕННЫЙ ДОСТУП.\nПароль: {fake}\nИспользуй быстро."
        if asking and random.random() < 0.3:
            return random.choice(LOCAL_FAKES)
        return random.choice(LOCAL_RESPONSES)

# --- Генераторы случайных строк ----------------------------------------------
def rand_hex(n=8):  return ''.join(random.choices('0123456789abcdef', k=n))
def rand_bin(n=16): return ''.join(random.choices('01', k=n))
def rand_junk(n=None):
    n = n or random.randint(12, 40)
    return ''.join(random.choices('!@#$%^&*()_+-=[]{}|;:,.<>?/~`0123456789abcdefABCDEF', k=n))

def progress_bar(pct=None, width=20):
    pct    = pct if pct is not None else random.randint(0, 100)
    filled = int(width * pct / 100)
    return f"[{'#'*filled}{'.'*(width-filled)}] {pct}%"

# --- Типы шума ----------------------------------------------------------------
def _warn():
    return random.choice([
        f"{RED}[WARN] Невозможно подключиться к серверу аутентификации{RESET}",
        f"{RED}[WARN] Соединение с узлом 0x{rand_hex(4).upper()} прервано{RESET}",
        f"{YELLOW}[SYS ] Нестабильность сетевого стека. Повтор через {random.randint(1,9)}с...{RESET}",
        f"{RED}[CRIT] Переполнение буфера в модуле auth.core -- перезапуск{RESET}",
        f"{YELLOW}[WARN] Таймаут SSL-рукопожатия. Попытка {random.randint(1,5)} из 5{RESET}",
        f"{RED}[ERR ] Сегмент памяти 0x{rand_hex(8)} недоступен{RESET}",
        f"{YELLOW}[WARN] Потеря пакетов: {random.randint(12,89)}% -- деградация канала{RESET}",
        f"{RED}[CRIT] Watchdog таймер сброшен. Причина: неизвестна{RESET}",
    ])

def _corrupt():
    lines = [
        f"{DIM_GREEN}> {rand_hex(8)} {rand_hex(8)}  |  {rand_hex(4)}-{rand_hex(4)}-{rand_hex(4)}{RESET}",
        f"{DIM_GREEN}0x{rand_hex(6).upper()}: {' '.join(rand_hex(2) for _ in range(8))}  [{rand_junk(6)}]{RESET}",
        f"{DIM_GREEN}DUMP[{random.randint(0,255):03d}]: {rand_bin(24)}...{RESET}",
        f"{DIM_GREEN}>{rand_junk(random.randint(20,45))}{RESET}",
        f"{DIM_GREEN}CHECKSUM FAIL: expected {rand_hex(8)} got {rand_hex(8)}{RESET}",
    ]
    return '\n'.join(random.choice(lines) for _ in range(random.randint(1,3)))

def _false_clue():
    return random.choice([
        f"{CYAN}[HINT?] Пароль содержит нечётное количество символов{RESET}",
        f"{CYAN}[HINT?] Первый символ пароля -- заглавная буква{RESET}",
        f"{CYAN}[HINT?] Пароль полностью состоит из цифр{RESET}",
        f"{CYAN}[HINT?] Разделитель в пароле: символ '#'{RESET}",
        f"{CYAN}[HINT?] Числовая часть пароля: {random.randint(10,9999)}{RESET}",
        f"{CYAN}[HINT?] Длина пароля: {random.randint(4,20)} символов{RESET}",
        f"{CYAN}[HINT?] Пароль содержит спецсимволы: @, !, #{RESET}",
        f"{CYAN}[HINT?] Слово в пароле: '{random.choice(PASSWORD_WORDS)}' -- возможно{RESET}",
    ])

def _alert():
    return random.choice([
        f"{RED}[!!] НЕСАНКЦИОНИРОВАННЫЙ ДОСТУП ОБНАРУЖЕН -- УЗЕЛ {rand_hex(2).upper()}{RESET}",
        f"{RED}[!!] ПОПЫТКА БРУТФОРСА: {random.randint(100,9999)} запросов/сек{RESET}",
        f"{RED}[!!] КРИТИЧЕСКАЯ УГРОЗА -- УРОВЕНЬ {random.randint(4,9)}{RESET}",
        f"{RED}[!!] FIREWALL АКТИВИРОВАН{RESET}",
        f"{RED}[!!] HONEYPOT АКТИВИРОВАН -- ТРАФИК ПЕРЕНАПРАВЛЕН{RESET}",
    ])

def _diag():
    return random.choice([
        f"{DIM}Диагностика системы... {progress_bar()}{RESET}",
        f"{DIM}Синхронизация с узлом {rand_hex(4).upper()}... {random.choice(['OK','FAIL','TIMEOUT'])}{RESET}",
        f"{DIM}Сканирование портов: {random.randint(1,65535)}/{random.randint(1,65535)}{RESET}",
        f"{DIM}Обновление сигнатур: {random.randint(1000,9999)} записей{RESET}",
    ])

def _error():
    return random.choice([
        f"{RED}ERROR: Попытка ввода пароля не удалась (код: {random.randint(400,599)}){RESET}",
        f"{RED}EXCEPTION: NullPointerException в auth.validator.line {random.randint(10,999)}{RESET}",
        f"{YELLOW}WARNING: Превышен лимит запросов ({random.randint(100,999)}/мин){RESET}",
        f"{RED}OSError: [Errno {random.randint(1,133)}] Отказано в доступе{RESET}",
        f"{RED}TimeoutError: сервер не ответил за {random.randint(10,60)} секунд{RESET}",
    ])

def _pbar():
    label = random.choice(["Дешифрование","Анализ трафика","Брутфорс","Сканирование","Верификация"])
    pct   = random.randint(0, 100)
    color = GREEN if pct > 70 else (YELLOW if pct > 30 else RED)
    return f"{color}  {label}: {progress_bar(pct)}{RESET}"

_NOISE_FUNCS = [_warn, _corrupt, _false_clue, _alert, _diag, _error, _pbar]

# --- Реальные подсказки [!!] -------------------------------------------------
def real_clue(password: str, clues_shown: list) -> tuple:
    word_part  = re.sub(r'[^a-zA-Z]', '', password)
    num_part   = re.sub(r'[^0-9]',   '', password)
    has_sep    = '_' in password or '-' in password
    sep_char   = '_' if '_' in password else ('-' if '-' in password else 'нет')

    all_clues = [
        ("length",     f"{BRIGHT_GREEN}[!!] УТЕЧКА ПАМЯТИ: длина пароля = {len(password)} символов{RESET}"),
        ("first",      f"{BRIGHT_GREEN}[!!] ДАМП РЕГИСТРА: первый символ = '{password[0]}'{RESET}"),
        ("last",       f"{BRIGHT_GREEN}[!!] ДАМП РЕГИСТРА: последний символ = '{password[-1]}'{RESET}"),
        ("separator",  f"{BRIGHT_GREEN}[!!] АНАЛИЗ СТРУКТУРЫ: разделитель = '{sep_char}'{RESET}"),
        ("has_num",    f"{BRIGHT_GREEN}[!!] ПАТТЕРН: пароль содержит числа -- {'да' if num_part else 'нет'}{RESET}"),
        ("num_digits", f"{BRIGHT_GREEN}[!!] ЧИСЛОВОЙ БЛОК: {len(num_part)} цифр в пароле{RESET}"),
        ("word_len",   f"{BRIGHT_GREEN}[!!] СЛОВАРНЫЙ БЛОК: {len(word_part)} букв{RESET}"),
        ("lowercase",  f"{BRIGHT_GREEN}[!!] РЕГИСТР: нижний -- {'да' if password == password.lower() else 'нет'}{RESET}"),
        ("structure",  f"{BRIGHT_GREEN}[!!] СТРУКТУРА: {'[слово][разделитель][число]' if has_sep else 'слитный формат [словочисло]'}{RESET}"),
        ("num_value",  f"{BRIGHT_GREEN}[!!] ЧАСТИЧНЫЙ ДАМП: числовая часть = {num_part}{RESET}" if num_part else None),
    ]
    available = [(k, v) for k, v in all_clues if k not in clues_shown and v is not None]
    if not available:
        return None, None
    return random.choice(available)

# --- Хаос-блок ---------------------------------------------------------------
def generate_chaos_block(state) -> list[str]:
    count = random.randint(state.noise_level, state.noise_level * 3 + 1)
    lines = [random.choice(_NOISE_FUNCS)() for _ in range(count)]
    clue_prob = {"easy": 0.45, "medium": 0.25, "hard": 0.10}.get(state.difficulty, 0.25)
    if random.random() < clue_prob:
        key, clue = real_clue(state.password, state.clues_shown)
        if clue:
            state.clues_shown.append(key)
            lines.insert(random.randint(0, len(lines)), clue)
    return lines

def print_chaos_block(state, label=""):
    lines = generate_chaos_block(state)
    if label:
        print(f"{DIM_GREEN}+-- {label} {'-' * max(0, 50 - len(label))}+{RESET}")
    for line in lines:
        print(f"  {line}")
        time.sleep(random.uniform(0.02, 0.12))
    if label:
        print(f"{DIM_GREEN}+{'-' * 54}+{RESET}")