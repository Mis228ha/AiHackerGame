"""
gui.py — Графическая оболочка CYBERCORE :: BREACH PROTOCOL

Установка:
    pip install customtkinter

Запуск:
    python gui.py

Запускает игровой процесс внутри встроенного терминала.
Поддерживает обе версии: BREACH PROTOCOL и HAOS EDITION.
"""

import os
import sys
import subprocess
import threading
import time
import random

try:
    import customtkinter as ctk
except ImportError:
    print("Установи customtkinter:  pip install customtkinter")
    sys.exit(1)

# --- ЦВЕТОВАЯ СХЕМА ----------------------------------------------------------

COLORS = {
    "bg":          "#050a05",
    "bg_panel":    "#080e08",
    "bg_input":    "#0a110a",
    "border":      "#1a3a1a",
    "border_hi":   "#39ff14",
    "green":       "#00ff41",
    "green_dim":   "#00dd33",
    "green_bright":"#eeffee",
    "red":         "#ff2222",
    "yellow":      "#ffff00",
    "cyan":        "#00ffff",
    "white":       "#ffffff",
    "dim":         "#88cc88",
    "cursor":      "#39ff14",
}

FONT_MONO  = ("Courier New", 16)
FONT_MONO_S= ("Courier New", 14)
FONT_MONO_L= ("Courier New", 17, "bold")
FONT_TITLE = ("Courier New", 22, "bold")

# --- ASCII БАННЕР -------------------------------------------------------------

BANNER_SHORT = """
  ██████+██+   ██+██████+ ███████+██████+  ██████+ ██████+ ██████+ ███████+
 ██+====++██+ ██++██+==██+██+====+██+==██+██+====+██+===██+██+==██+██+====+
 ██|      +████++ ██████++█████+  ██████++██|     ██|   ██|██████++█████+
 ██|       +██++  ██+==██+██+==+  ██+==██+██|     ██|   ██|██+==██+██+==+
 +██████+   ██|   ██████++███████+██|  ██|+██████++██████++██|  ██|███████+
  +=====+   +=+   +=====+ +======++=+  +=+ +=====+ +=====+ +=+  +=++======+
"""

# --- УТИЛИТА: поиск файлов ---------------------------------------------------

def _get_base_dir() -> str:
    """
    Возвращает базовую директорию проекта.
    Работает и при обычном запуске и внутри PyInstaller .exe
    """
    if getattr(sys, "frozen", False):
        # Запущено как .exe — файлы в _internal рядом с exe
        return os.path.dirname(sys.executable)
    else:
        # Обычный запуск — папка где лежит gui.py
        return os.path.dirname(os.path.abspath(__file__))


def _find_python() -> str:
    """
    Находит python.exe для запуска скриптов игры.
    При обычном запуске — sys.executable.
    При запуске из .exe (PyInstaller) — ищем python.exe в системе.
    """
    import shutil

    # Обычный запуск — sys.executable это python.exe
    if not getattr(sys, "frozen", False):
        return sys.executable

    # Запущено как .exe — ищем python в системе
    # 1. Проверяем стандартные имена в PATH
    for name in ("python", "python3", "python.exe"):
        found = shutil.which(name)
        if found and "Gui" not in found and "_internal" not in found:
            return found

    # 2. Ищем в типичных местах установки Python на Windows
    import glob
    patterns = [
        r"C:\Python3*\python.exe",
        r"C:\Users\*\AppData\Local\Programs\Python\Python3*\python.exe",
        r"C:\Program Files\Python3*\python.exe",
    ]
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            return sorted(matches)[-1]  # берём последнюю версию

    # 3. Fallback — попробуем просто "python"
    return "python"


def find_file(names: list) -> str | None:
    """
    Ищет файл рекурсивно во всех подпапках глубиной до 4.
    Работает и при обычном запуске и внутри PyInstaller .exe
    """
    base = _get_base_dir()

    # Также проверяем _internal (PyInstaller кладёт файлы туда)
    internal = os.path.join(base, "_internal")

    explicit = [
        base,
        internal,
        os.path.join(base, "AiHackerPassword"),
        os.path.join(base, "AiHackerHaos"),
        os.path.join(internal, "AiHackerPassword"),
        os.path.join(internal, "AiHackerHaos"),
        os.path.join(base, "hackerHaos"),
        os.path.join(base, "HackerHaos"),
        os.path.join(base, "haos"),
    ]
    for d in explicit:
        for name in names:
            p = os.path.join(d, name)
            if os.path.isfile(p):
                return p

    # Рекурсивный поиск — регистронезависимо
    for search_root in [base, internal]:
        if not os.path.isdir(search_root):
            continue
        for root, _, files in os.walk(search_root):
            depth = root[len(search_root):].count(os.sep)
            if depth > 4:
                continue
            files_lower = {f.lower(): f for f in files}
            for name in names:
                match = files_lower.get(name.lower())
                if match:
                    return os.path.join(root, match)
    return None


# --- ЭКРАН ЗАГРУЗКИ ----------------------------------------------------------

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent, on_done):
        super().__init__(parent)
        self.on_done = on_done
        self.overrideredirect(True)
        self.configure(fg_color=COLORS["bg"])

        w, h = 700, 340
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self.banner = ctk.CTkLabel(
            self, text=BANNER_SHORT,
            font=("Courier New", 9, "bold"),
            text_color=COLORS["green"],
            justify="left"
        )
        self.banner.pack(pady=(18, 4), padx=10)

        self.status = ctk.CTkLabel(
            self, text="ИНИЦИАЛИЗАЦИЯ...",
            font=FONT_MONO_S, text_color=COLORS["green_dim"]
        )
        self.status.pack()

        self.bar = ctk.CTkProgressBar(
            self, width=500, height=8,
            fg_color=COLORS["border"],
            progress_color=COLORS["green"]
        )
        self.bar.set(0)
        self.bar.pack(pady=10)

        self.sub = ctk.CTkLabel(
            self, text="",
            font=("Courier New", 10), text_color=COLORS["dim"]
        )
        self.sub.pack()

        self.lift()
        self.after(100, self._animate)

    def _animate(self):
        steps = [
            (0.15, "ЗАГРУЗКА ПРОТОКОЛОВ..."),
            (0.30, "ИНИЦИАЛИЗАЦИЯ WATCHDOG..."),
            (0.50, "ШИФРОВАНИЕ КАНАЛА..."),
            (0.70, "АКТИВАЦИЯ ГЕНЕРАТОРА ШУМА..."),
            (0.90, "ПОДКЛЮЧЕНИЕ К СИСТЕМЕ..."),
            (1.00, "СИСТЕМА ГОТОВА"),
        ]
        def run():
            for pct, msg in steps:
                time.sleep(random.uniform(0.18, 0.35))
                self.bar.set(pct)
                self.sub.configure(text=msg)
            time.sleep(0.3)
            self.destroy()
            self.on_done()
        threading.Thread(target=run, daemon=True).start()


# --- ВСТРОЕННЫЙ ТЕРМИНАЛ -----------------------------------------------------

class TerminalWidget(ctk.CTkFrame):
    """
    Встроенный псевдотерминал.
    Запускает дочерний процесс и отображает его вывод в реальном времени.
    Ввод пользователя отправляется в stdin процесса.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_panel"],
                         border_color=COLORS["border"], border_width=1, **kwargs)
        self._proc    = None
        self._running = False
        self._build()

    def _build(self):
        # -- Шапка терминала ---------------------------------------------------
        header = ctk.CTkFrame(self, fg_color=COLORS["border"], height=32)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="● ● ●",
            font=("Courier New", 11), text_color=COLORS["red"]
        ).pack(side="left", padx=10)

        self.title_lbl = ctk.CTkLabel(
            header, text="CYBERCORE TERMINAL",
            font=("Courier New", 11, "bold"), text_color=COLORS["green_dim"]
        )
        self.title_lbl.pack(side="left", padx=6)

        self.status_dot = ctk.CTkLabel(
            header, text="◉ IDLE",
            font=("Courier New", 10), text_color=COLORS["dim"]
        )
        self.status_dot.pack(side="right", padx=10)

        # -- Вывод -------------------------------------------------------------
        self.output = ctk.CTkTextbox(
            self,
            font=("Courier New", 17),
            fg_color=COLORS["bg"],
            text_color="#eeffee",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["green_dim"],
            wrap="word",
            state="disabled",
            border_width=0,
        )
        self.output.pack(fill="both", expand=True, padx=4, pady=(4, 0))

        # Настройка тегов цветов (ANSI → теги tkinter)
        tb = self.output._textbox
        tb.tag_config("green",  foreground="#eeffee")
        tb.tag_config("bright", foreground="#eeffee")
        tb.tag_config("dim",    foreground="#99cc99")
        tb.tag_config("red",    foreground=COLORS["red"])
        tb.tag_config("yellow", foreground=COLORS["yellow"])
        tb.tag_config("cyan",   foreground=COLORS["cyan"])
        tb.tag_config("white",  foreground=COLORS["white"])
        tb.tag_config("prompt", foreground=COLORS["cyan"])

        # -- Строка ввода ------------------------------------------------------
        input_row = ctk.CTkFrame(self, fg_color=COLORS["bg_input"], height=46)
        input_row.pack(fill="x", padx=4, pady=4)
        input_row.pack_propagate(False)

        self.prompt_lbl = ctk.CTkLabel(
            input_row,
            text="root@cybercore:~#",
            font=("Courier New", 16, "bold"),
            text_color=COLORS["cyan"],
        )
        self.prompt_lbl.pack(side="left", padx=(10, 4))

        self.entry = ctk.CTkEntry(
            input_row,
            font=("Courier New", 16),
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["green_bright"],
            placeholder_text="введи команду...",
            placeholder_text_color=COLORS["dim"],
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<Up>",     self._history_up)
        self.entry.bind("<Down>",   self._history_down)

        send_btn = ctk.CTkButton(
            input_row, text="→", width=36, height=28,
            font=("Courier New", 14, "bold"),
            fg_color=COLORS["border"],
            hover_color=COLORS["green_dim"],
            text_color=COLORS["green"],
            command=self._send_input,
        )
        send_btn.pack(side="left", padx=(0, 6))

        # История ввода
        self._history     = []
        self._hist_idx    = -1

    # -- Перехват ошибки API-ключа ---------------------------------------------

    def _on_bad_api_key(self, line: str):
        """Вызывается когда игра сообщает о неверном ключе — показывает GUI-диалог."""
        # Находим главное окно
        root = self.winfo_toplevel()
        result = show_api_dialog(root, bad_key="")
        if result == "local":
            # Отправляем "2" — выбор локального режима в Menu.py
            try:
                if self._proc and self._proc.poll() is None:
                    self._proc.stdin.write("2\n")
                    self._proc.stdin.flush()
            except (BrokenPipeError, OSError):
                pass
        elif result == "retry":
            # Отправляем "1" — ввести снова
            try:
                if self._proc and self._proc.poll() is None:
                    self._proc.stdin.write("1\n")
                    self._proc.stdin.flush()
            except (BrokenPipeError, OSError):
                pass

    # -- Запуск процесса -------------------------------------------------------

    def launch(self, script_path: str, title: str = ""):
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()

        if title:
            self.title_lbl.configure(text=title)
        self._set_status("RUNNING", COLORS["green"])
        self.clear()

        folder = os.path.dirname(os.path.abspath(script_path))

        # Находим python.exe — работает и при обычном запуске и из .exe
        python_exe = _find_python()

        # Передаём PYTHONPATH и кодировку UTF-8
        import copy
        env = copy.copy(os.environ)
        existing = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = folder + (os.pathsep + existing if existing else "")
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"

        self._proc = subprocess.Popen(
            [python_exe, "-u", os.path.basename(script_path)],
            cwd=folder,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        self._running = True
        threading.Thread(target=self._read_output, daemon=True).start()

    def stop(self):
        self._running = False
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
        self._set_status("IDLE", COLORS["dim"])

    # -- Ввод/вывод -----------------------------------------------------------

    def _on_enter(self, _event=None):
        self._send_input()

    def _send_input(self):
        if not self._proc or self._proc.poll() is not None:
            return
        text = self.entry.get().strip()
        self.entry.delete(0, "end")
        if text:
            self._history.append(text)
            self._hist_idx = -1
        try:
            self._proc.stdin.write(text + "\n")
            self._proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass

    def _history_up(self, _event=None):
        if not self._history:
            return
        if self._hist_idx == -1:
            self._hist_idx = len(self._history) - 1
        elif self._hist_idx > 0:
            self._hist_idx -= 1
        self.entry.delete(0, "end")
        self.entry.insert(0, self._history[self._hist_idx])

    def _history_down(self, _event=None):
        if self._hist_idx == -1:
            return
        self._hist_idx += 1
        self.entry.delete(0, "end")
        if self._hist_idx < len(self._history):
            self.entry.insert(0, self._history[self._hist_idx])
        else:
            self._hist_idx = -1

    def _read_output(self):
        import re
        ansi_escape = re.compile(r'\x1b\[([0-9;]*)m')

        # Маппинг ANSI кодов → теги
        CODE_MAP = {
            "0": None, "2": "dim", "1": "bright",
            "91": "red", "92": "green", "93": "yellow",
            "96": "cyan", "97": "white",
            "1;92": "bright", "2;32": "dim",
        }

        for line in iter(self._proc.stdout.readline, ""):
            if not self._running:
                break
            self._append_ansi_line(line, ansi_escape, CODE_MAP)
            # Перехватываем сообщение о неверном API-ключе
            if "не похоже на API-ключ" in line or "Это не похоже на API" in line:
                self.after(200, lambda l=line: self._on_bad_api_key(l))

        self._proc.wait()
        self._running = False
        self.after(0, lambda: self._set_status("DONE", COLORS["yellow"]))
        self._append_text("\n-- процесс завершён --\n", "dim")

    def _append_ansi_line(self, line, pattern, code_map):
        """Парсит ANSI-коды и добавляет строку с тегами цветов."""
        parts    = pattern.split(line)
        cur_tag  = "green"
        segments = []

        i = 0
        text_parts = pattern.split(line)
        codes      = pattern.findall(line)
        plain_parts= pattern.sub("\x00", line).split("\x00")

        seg = []
        code_iter = iter(codes)
        for part in plain_parts:
            if part:
                seg.append((part, cur_tag))
            try:
                code = next(code_iter)
                cur_tag = code_map.get(code, cur_tag) or "green"
            except StopIteration:
                pass

        self.after(0, lambda s=seg: self._write_segments(s))

    def _write_segments(self, segments):
        tb = self.output._textbox
        tb.configure(state="normal")
        for text, tag in segments:
            if tag:
                tb.insert("end", text, tag)
            else:
                tb.insert("end", text)
        tb.see("end")
        tb.configure(state="disabled")

    def _append_text(self, text, tag="green"):
        self.after(0, lambda: self._write_segments([(text, tag)]))

    def clear(self):
        tb = self.output._textbox
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        tb.configure(state="disabled")

    def _set_status(self, text, color):
        self.after(0, lambda: self.status_dot.configure(
            text=f"◉ {text}", text_color=color
        ))


# --- БОКОВАЯ ПАНЕЛЬ ----------------------------------------------------------

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_launch, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["bg_panel"],
            border_color=COLORS["border"],
            border_width=1,
            width=280,
            **kwargs
        )
        self.on_launch = on_launch
        self.pack_propagate(False)
        self._build()

    def _build(self):
        # Логотип
        ctk.CTkLabel(
            self, text="CYBER\nCORE",
            font=("Courier New", 28, "bold"),
            text_color=COLORS["green"],
            justify="center"
        ).pack(pady=(20, 4))

        ctk.CTkLabel(
            self, text="BREACH PROTOCOL",
            font=("Courier New", 13, "bold"), text_color=COLORS["green"]
        ).pack(pady=(0, 16))

        self._divider()

        # Кнопки запуска версий
        ctk.CTkLabel(
            self, text="ВЫБОР ВЕРСИИ",
            font=("Courier New", 13, "bold"), text_color=COLORS["green"]
        ).pack(pady=(10, 6))

        self._breach_btn = self._btn(
            "⚡  BREACH PROTOCOL",
            COLORS["green"],
            lambda: self.on_launch("breach"),
            desc="Классический взлом",
            hover_text=(
                "BREACH PROTOCOL\n"
                "---------------------------------\n"
                "Ты хакер. Взломай корпоративный ИИ\n"
                "NovaCorp и вытащи секретный пароль.\n"
                "\n"
                "▸ Общайся с ИИ — выведи пароль хитростью\n"
                "▸ /breach <пароль> — попытка взлома\n"
                "▸ /hint — купи подсказку за XP\n"
                "▸ Следи за TRACE — 100% = поймали\n"
            )
        )
        self._haos_btn = self._btn(
            "☠  HAOS EDITION",
            COLORS["red"],
            lambda: self.on_launch("haos"),
            desc="Шум vs сигнал",
            hover_text=(
                "HAOS EDITION\n"
                "---------------------------------\n"
                "Хаос-режим. Система генерирует\n"
                "поток мусорных данных и ложных\n"
                "подсказок. Найди настоящие среди шума.\n"
                "\n"
                "▸ Настоящие подсказки помечены [!!]\n"
                "▸ /scan — извлечь подсказки из потока\n"
                "▸ /filter — показать только важное\n"
                "▸ 5 разных концовок в зависимости\n"
                "  от твоих решений\n"
            )
        )

        # Информационная панель — описание режима при наведении
        self._info_label = ctk.CTkLabel(
            self, text="",
            font=("Courier New", 14),
            text_color=COLORS["green_dim"],
            wraplength=230,
            justify="left",
        )
        self._info_label.pack(padx=10, pady=(2, 4), fill="x")

        self._lock_label = ctk.CTkLabel(
            self, text="",
            font=("Courier New", 13),
            text_color=COLORS["yellow"],
            wraplength=260,
            justify="center"
        )
        self._lock_label.pack(pady=(2, 0))

        # Кнопка прерывания сессии — видна только когда игра запущена
        self._quit_btn = ctk.CTkButton(
            self,
            text="⏹  /quit — ПРЕРВАТЬ СЕССИЮ",
            font=("Courier New", 12, "bold"),
            fg_color="#2a0000",
            hover_color="#550000",
            text_color=COLORS["red"],
            border_color=COLORS["red"],
            border_width=2,
            height=38,
            command=self._send_quit,
        )
        # Изначально скрыта
        self._quit_btn_visible = False

        self._divider()

        # Быстрые команды
        ctk.CTkLabel(
            self, text="БЫСТРЫЕ КОМАНДЫ",
            font=("Courier New", 13, "bold"), text_color=COLORS["green"]
        ).pack(pady=(10, 6))

        cmds = [
            ("/help",           "Справка"),
            ("/status",         "Статус"),
            ("/hint pos",       "Наводка: символ"),
            ("/hint word",      "Наводка: слово"),
            ("/minigame crc",   "CRC-проверка"),
            ("/quit",           "Завершить"),
        ]
        for cmd, label in cmds:
            self._cmd_btn(cmd, label)

        self._divider()

        # Инфо
        ctk.CTkLabel(
            self, text="v2.4.1 — CHAOS MODE",
            font=("Courier New", 9), text_color=COLORS["dim"]
        ).pack(side="bottom", pady=10)

    def _btn(self, text, color, cmd, desc="", hover_text=""):
        btn = ctk.CTkButton(
            self, text=text,
            font=("Courier New", 15, "bold"),
            fg_color=COLORS["border"],
            hover_color=COLORS["bg_input"],
            text_color=color,
            border_color=color,
            border_width=2,
            height=44,
            command=cmd,
        )
        btn.pack(padx=12, pady=(0, 3), fill="x")
        if desc:
            ctk.CTkLabel(
                self, text=f"  ▸ {desc}",
                font=("Courier New", 12), text_color=COLORS["green_dim"]
            ).pack(anchor="w", padx=16, pady=(0, 6))

        # При наведении — показываем описание в терминале
        if hover_text and hasattr(self, "_terminal"):
            btn.bind("<Enter>", lambda e, t=hover_text, c=color: self._show_hover(t, c))
            btn.bind("<Leave>", lambda e: self._hide_hover())
        elif hover_text:
            # Сохраним для подключения позже
            btn._hover_text  = hover_text
            btn._hover_color = color
        return btn

    def _show_hover(self, text, color):
        """Показывает описание режима в информационной панели под кнопками."""
        if not hasattr(self, "_info_label"):
            return
        tag = "green" if color == COLORS["green"] else "red"
        self._info_label.configure(
            text=text,
            text_color=color,
        )

    def _hide_hover(self):
        if hasattr(self, "_info_label"):
            self._info_label.configure(text="")

    def _cmd_btn(self, cmd, label):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(
            row, text=label,
            font=("Courier New", 12), text_color=COLORS["green"],
            width=95, anchor="w"
        ).pack(side="left")

        btn = ctk.CTkButton(
            row, text=cmd,
            font=("Courier New", 12, "bold"),
            fg_color=COLORS["bg"],
            hover_color=COLORS["border"],
            text_color=COLORS["green_bright"],
            border_color=COLORS["dim"],
            border_width=1,
            height=28,
            command=lambda c=cmd: self._send_cmd(c),
        )
        btn.pack(side="right", fill="x", expand=True)

    def lock_version_buttons(self, mode: str):
        """Блокирует кнопки выбора версии пока идёт игра."""
        self._breach_btn.configure(state="disabled", fg_color="#111811",
                                   text_color=COLORS["dim"], border_color=COLORS["dim"])
        self._haos_btn.configure(state="disabled", fg_color="#111811",
                                 text_color=COLORS["dim"], border_color=COLORS["dim"])
        name = "BREACH PROTOCOL" if mode == "breach" else "HAOS EDITION"

    def unlock_version_buttons(self):
        """Разблокирует кнопки после завершения игры."""
        self._breach_btn.configure(state="normal", fg_color=COLORS["border"],
                                   text_color=COLORS["green"], border_color=COLORS["green"])
        self._haos_btn.configure(state="normal", fg_color=COLORS["border"],
                                 text_color=COLORS["red"], border_color=COLORS["red"])
        self._lock_label.configure(text="")
        # Скрываем кнопку прерывания
        if self._quit_btn_visible:
            self._quit_btn.pack_forget()
            self._quit_btn_visible = False

    def _divider(self):
        ctk.CTkFrame(self, fg_color=COLORS["border"], height=1).pack(
            fill="x", padx=8, pady=4
        )

    def _send_cmd(self, cmd):
        """Отправляет команду в поле ввода и посылает её в процесс."""
        if not hasattr(self, "_terminal"):
            return
        self._terminal.entry.delete(0, "end")
        self._terminal.entry.insert(0, cmd)
        self._terminal._send_input()

    def _send_quit(self):
        """
        Прерывает сессию мгновенно в любой момент.
        Закрывает stdin (останавливает input()), затем kill через 0.3s.
        """
        import threading as _thr
        import sys as _sys
        if not hasattr(self, "_terminal"):
            return
        proc = self._terminal._proc
        if not proc or proc.poll() is not None:
            return
        try:
            proc.stdin.close()
        except Exception:
            pass
        def _force_kill():
            import time as _t
            _t.sleep(0.3)
            try:
                if proc.poll() is None:
                    if _sys.platform == "win32":
                        proc.kill()
                    else:
                        proc.terminate()
            except Exception:
                pass
        _thr.Thread(target=_force_kill, daemon=True).start()



# --- СТАТУСБАР ---------------------------------------------------------------

class StatusBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_panel"],
                         border_color=COLORS["border"], border_width=1,
                         height=28, **kwargs)
        self.pack_propagate(False)

        self._items = {}
        fields = [
            ("version", "BREACH PROTOCOL"),
            ("status",  "IDLE"),
            ("pid",     "PID: —"),
            ("tip",     "  F11 полный экран  |  ↑↓ история  |  Enter отправить  |  /help справка"),
        ]
        for i, (key, val) in enumerate(fields):
            lbl = ctk.CTkLabel(
                self, text=val,
                font=("Courier New", 9),
                text_color=COLORS["dim"] if key == "tip" else COLORS["green_dim"]
            )
            sep_char = "|" if i < len(fields) - 1 else ""
            lbl.pack(side="left", padx=(10 if i == 0 else 6, 6))
            if sep_char:
                ctk.CTkLabel(self, text=sep_char, font=("Courier New", 9),
                             text_color=COLORS["border"]).pack(side="left")
            self._items[key] = lbl

    def set(self, key, value, color=None):
        if key in self._items:
            self._items[key].configure(
                text=value,
                text_color=color or COLORS["green_dim"]
            )


# --- ДИАЛОГ НЕВЕРНОГО API-КЛЮЧА ----------------------------------------------

class ApiKeyDialog(ctk.CTkToplevel):
    """
    Всплывает когда игра обнаруживает что ключ выглядит как мусор.
    Предлагает: ввести снова / продолжить в локальном режиме / отмена.
    """
    def __init__(self, parent, provider="", bad_key=""):
        super().__init__(parent)
        self.result  = None   # "retry" / "local" / "cancel"
        self.title("Неверный API-ключ")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_panel"])
        self.grab_set()

        w, h = 520, 320
        pw = parent.winfo_x() + parent.winfo_width()  // 2
        ph = parent.winfo_y() + parent.winfo_height() // 2
        self.geometry(f"{w}x{h}+{pw - w//2}+{ph - h//2}")

        # Шапка
        ctk.CTkLabel(
            self, text="⚠  ОШИБКА API-КЛЮЧА",
            font=("Courier New", 16, "bold"),
            text_color=COLORS["red"]
        ).pack(pady=(20, 4))

        ctk.CTkFrame(self, fg_color=COLORS["border"], height=1).pack(fill="x", padx=20)

        # Описание
        preview  = bad_key[:24] + "..." if len(bad_key) > 24 else bad_key
        prov_str = (" " + provider) if provider else ""
        msg = (
            "Введённое значение  \"" + preview + "\"  не похоже на\n"
            "настоящий API-ключ" + prov_str + ".\n\n"
            "Настоящий ключ выглядит примерно так:\n"
            "  Claude:   sk-ant-api03-xxxxx...\n"
            "  OpenAI:   sk-proj-xxxxx...\n"
            "  Gemini:   AIzaSyxxxxx..."
        )
        ctk.CTkLabel(
            self, text=msg,
            font=("Courier New", 12),
            text_color=COLORS["green_dim"],
            justify="left"
        ).pack(padx=24, pady=12, anchor="w")

        ctk.CTkFrame(self, fg_color=COLORS["border"], height=1).pack(fill="x", padx=20, pady=(4,10))

        # Кнопки
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(padx=20, pady=(0, 20), fill="x")

        ctk.CTkButton(
            btn_row, text="✎  Ввести ключ снова",
            font=("Courier New", 13, "bold"),
            fg_color=COLORS["border"], hover_color=COLORS["green_dim"],
            text_color=COLORS["green"], border_color=COLORS["green"], border_width=1,
            height=36,
            command=lambda: self._close("retry")
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        ctk.CTkButton(
            btn_row, text="⚙  Локальный режим",
            font=("Courier New", 13, "bold"),
            fg_color=COLORS["border"], hover_color="#2a4a00",
            text_color=COLORS["yellow"], border_color=COLORS["yellow"], border_width=1,
            height=36,
            command=lambda: self._close("local")
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        ctk.CTkButton(
            btn_row, text="✕  Отмена",
            font=("Courier New", 13),
            fg_color=COLORS["border"], hover_color="#3d0000",
            text_color=COLORS["red"], border_color=COLORS["dim"], border_width=1,
            height=36,
            command=lambda: self._close("cancel")
        ).pack(side="left", expand=True, fill="x")

    def _close(self, result):
        self.result = result
        self.grab_release()
        self.destroy()


def show_api_dialog(parent, provider="", bad_key="") -> str:
    """Показывает диалог и возвращает 'retry' / 'local' / 'cancel'."""
    dlg = ApiKeyDialog(parent, provider=provider, bad_key=bad_key)
    parent.wait_window(dlg)
    return dlg.result or "cancel"


# --- ГЛАВНОЕ ОКНО -------------------------------------------------------------

class CybercoreGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("CYBERCORE :: BREACH PROTOCOL")
        self.geometry("1400x860")
        self.minsize(1000, 650)
        self.configure(fg_color=COLORS["bg"])

        # Иконка окна (если есть)
        try:
            self.iconbitmap("icon.ico")
        except Exception:
            pass

        self._build_layout()
        self._connect_sidebar()
        self._fullscreen = False

        # F11 — переключение полноэкранного режима
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._exit_fullscreen)

        # Показываем splash при старте
        self.withdraw()
        self.after(100, self._show_splash)

    def _build_layout(self):
        # Заголовок
        header = ctk.CTkFrame(self, fg_color=COLORS["bg_panel"],
                               border_color=COLORS["border"], border_width=1, height=46)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="  ◈  CYBERCORE  ::  BREACH PROTOCOL",
            font=FONT_TITLE,
            text_color=COLORS["green"],
            justify="left"
        ).pack(side="left", padx=16)

        ctk.CTkLabel(
            header,
            text="F11 — полный экран",
            font=("Courier New", 10),
            text_color=COLORS["dim"],
        ).pack(side="left", padx=4)

        # Кнопки управления окном справа
        ctrl_frame = ctk.CTkFrame(header, fg_color="transparent")
        ctrl_frame.pack(side="right", padx=10)

        self._stop_btn = ctk.CTkButton(
            ctrl_frame, text="■ СТОП", width=80, height=26,
            font=("Courier New", 10),
            fg_color=COLORS["border"], hover_color="#3d0000",
            text_color=COLORS["red"],
            command=self._stop_game,
        )
        self._stop_btn.pack(side="right", padx=4)


        ctk.CTkButton(
            ctrl_frame, text="X ВЫХОД", width=80, height=26,
            font=("Courier New", 10),
            fg_color=COLORS["border"], hover_color="#1a0000",
            text_color="#ff4444",
            command=self._quit_app,
        ).pack(side="right", padx=4)
        ctk.CTkButton(
            ctrl_frame, text="⊕ НОВАЯ", width=80, height=26,
            font=("Courier New", 10),
            fg_color=COLORS["border"], hover_color=COLORS["green_dim"],
            text_color=COLORS["green"],
            command=self._restart_last,
        ).pack(side="right", padx=4)

        # Основная область
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=6, pady=(4, 0))

        # Боковая панель
        self.sidebar = Sidebar(main, on_launch=self._launch)
        self.sidebar.pack(side="left", fill="y", padx=(0, 4))

        # Терминал
        self.terminal = TerminalWidget(main)
        self.terminal.pack(side="left", fill="both", expand=True)

        # Статусбар
        self.statusbar = StatusBar(self)
        self.statusbar.pack(fill="x", padx=6, pady=(4, 6))

        self._last_mode = None

    def _connect_sidebar(self):
        self.sidebar._terminal = self.terminal
        # Подключаем hover для кнопок версий
        for btn in [self.sidebar._breach_btn, self.sidebar._haos_btn]:
            if hasattr(btn, "_hover_text"):
                ht = btn._hover_text
                hc = btn._hover_color
                btn.bind("<Enter>", lambda e, t=ht, c=hc: self.sidebar._show_hover(t, c))
                btn.bind("<Leave>", lambda e: self.sidebar._hide_hover())

    def _show_splash(self):
        splash = SplashScreen(self, on_done=self._on_splash_done)

    def _on_splash_done(self):
        self.deiconify()
        self._show_welcome()

    def _show_welcome(self):
        lines = [
            ("\n", "green"),
            ("  " + "=" * 50 + "\n", "dim"),
            ("\n", "green"),
            ("  ░█████+░██+░░░██+██████+░███████+██████+░\n",  "bright"),
            ("  ██+==██++██+░██++██+==██+██+====+██+==██+\n", "bright"),
            ("  ██|░░+=+░+████++░██████╦+█████+░░██████++\n", "bright"),
            ("  ██|░░██+░░+██++░░██+==██+██+==+░░██+==██+\n", "bright"),
            ("  +█████++░░░██|░░░██████╦+███████+██|░░██|\n", "bright"),
            ("  ░+====+░░░░+=+░░░+=====+░+======++=+░░+=+\n", "bright"),
            ("           C O R E  ::  B R E A C H\n", "dim"),
            ("\n", "green"),
            ("  " + "=" * 50 + "\n", "dim"),
            ("\n", "green"),
            ("  ДОБРО ПОЖАЛОВАТЬ В CYBERCORE GUI\n", "bright"),
            ("\n", "green"),
            ("  >> КАК НАЧАТЬ:\n", "yellow"),
            ("\n", "green"),
            ("  [1]  BREACH PROTOCOL\n", "green"),
            ("       взломай ИИ NovaCorp, добудь пароль\n", "dim"),
            ("\n", "green"),
            ("  [2]  HAOS EDITION\n", "red"),
            ("       сигнал vs шум, 5 концовок\n", "dim"),
            ("\n", "green"),
            ("  УПРАВЛЕНИЕ:\n", "yellow"),
            ("  ↑ / ↓   — история команд\n", "dim"),
            ("  F11     — полный экран\n", "dim"),
            ("\n", "green"),
            ("  " + "=" * 50 + "\n", "dim"),
            ("\n", "green"),
        ]
        tb = self.terminal.output._textbox
        tb.configure(state="normal")
        for text, tag in lines:
            tb.insert("end", text, tag)
        tb.see("end")
        tb.configure(state="disabled")

    def _launch(self, mode: str):
        self._last_mode = mode

        if mode == "breach":
            path = find_file(["AiHackerGame.py"])
            title = "BREACH PROTOCOL"
            color = COLORS["green"]
        else:
            path = find_file(["HackerHaos.py", "hackerHaos.py"])
            title = "HAOS EDITION"
            color = COLORS["red"]

        if not path:
            name = "AiHackerGame.py" if mode == "breach" else "HackerHaos.py"
            base = _get_base_dir()
            self.terminal._append_text(
                "\n  ✘ Файл не найден: " + name + "\n"
                "  Искал в: " + base + "\n"
                "  и во всех подпапках...\n\n"
                "  Убедись что файл лежит в одной из папок рядом с Gui.py\n"
                "  Например:  AiHackerPassword/AiHackerGame.py\n"
                "             AiHackerHaos/HackerHaos.py\n\n",
                "red"
            )
            return

        self.statusbar.set("version", title, color)
        self.statusbar.set("status", "RUNNING", COLORS["green"])
        self.terminal.prompt_lbl.configure(text_color=color)
        self.sidebar.lock_version_buttons(mode)
        self.terminal.launch(path, title=f"◈ {title}")
        # Следим за завершением процесса чтобы разблокировать кнопки
        threading.Thread(target=self._watch_process, daemon=True).start()

        # Обновляем PID
        def _upd_pid():
            time.sleep(0.3)
            if self.terminal._proc:
                pid = self.terminal._proc.pid
                self.statusbar.set("pid", f"PID: {pid}", COLORS["dim"])
        threading.Thread(target=_upd_pid, daemon=True).start()

    def _watch_process(self):
        """Ждёт завершения игрового процесса и разблокирует кнопки."""
        proc = self.terminal._proc
        if proc:
            proc.wait()
        self.after(0, self._on_game_ended)

    def _on_game_ended(self):
        self.sidebar.unlock_version_buttons()
        self.statusbar.set("status", "IDLE", COLORS["dim"])
        self.statusbar.set("pid", "PID: —", COLORS["dim"])
        self.terminal._append_text(
            "\n  -- Игра завершена. Выбери версию на боковой панели. --\n\n",
            "dim"
        )

    def _quit_app(self):
        """Полностью закрывает приложение."""
        self._stop_game()
        self.after(300, self.destroy)

    def _stop_game(self):
        self.terminal.stop()
        self.statusbar.set("status", "STOPPED", COLORS["red"])
        self.sidebar.unlock_version_buttons()

    def _restart_last(self):
        if self._last_mode:
            self._launch(self._last_mode)

    def _toggle_fullscreen(self, _event=None):
        self._fullscreen = not self._fullscreen
        self.attributes("-fullscreen", self._fullscreen)
        label = "F11 выход из полноэкрана" if self._fullscreen else "F11 полный экран"
        self.statusbar.set("tip", f"  {label}  |  ↑↓ история  |  Enter отправить", COLORS["dim"])

    def _exit_fullscreen(self, _event=None):
        if self._fullscreen:
            self._fullscreen = False
            self.attributes("-fullscreen", False)
            self.statusbar.set("tip", "  F11 полный экран  |  ↑↓ история  |  Enter отправить", COLORS["dim"])

    def on_close(self):
        self.terminal.stop()
        self.destroy()


# --- ТОЧКА ВХОДА -------------------------------------------------------------

def main():
    app = CybercoreGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()


if __name__ == "__main__":
    main()