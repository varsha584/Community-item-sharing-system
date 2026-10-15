import tkinter as tk
from tkinter import ttk

BG = "#F4F6F3"
PRIMARY = "#1F4E4A"
PRIMARY_HOVER = "#2C6B65"
ACCENT = "#E8A33D"
TEXT = "#1E2B2A"
MUTED = "#6B7A78"
CARD = "#FFFFFF"
BORDER = "#DDE3DF"
DANGER = "#B3402F"
DANGER_HOVER = "#963322"
GREEN = "#2E8B57"
AMBER = "#C77D12"
FONT = "Segoe UI"

CATEGORIES = [
    "Electronics", "Tools", "Books", "Kitchen",
    "Clothing", "Sports", "Toys", "Other"
]


def setup(win, title, size):
    win.title(title)
    win.configure(bg=BG)
    width, height = (int(v) for v in size.split("x"))
    x = (win.winfo_screenwidth() - width) // 2
    y = max(0, (win.winfo_screenheight() - height) // 2 - 20)
    win.geometry(f"{width}x{height}+{x}+{y}")


def header(win, title, subtitle=""):
    bar = tk.Frame(win, bg=PRIMARY)
    bar.pack(fill="x")
    tk.Label(bar, text=title, font=(FONT, 20, "bold"),
             bg=PRIMARY, fg="white").pack(
        anchor="w", padx=24, pady=(16, 2 if subtitle else 16))
    if subtitle:
        tk.Label(bar, text=subtitle, font=(FONT, 10),
                 bg=PRIMARY, fg="#BFD6D2").pack(
            anchor="w", padx=24, pady=(0, 14))
    tk.Frame(win, bg=ACCENT, height=3).pack(fill="x")


def card(win, padx=24, pady=18):
    outer = tk.Frame(win, bg=BG)
    outer.pack(fill="both", expand=True, padx=padx, pady=pady)
    box = tk.Frame(outer, bg=CARD, highlightbackground=BORDER,
                   highlightthickness=1)
    box.pack(fill="both", expand=True)
    inner = tk.Frame(box, bg=CARD)
    inner.pack(fill="both", expand=True, padx=22, pady=18)
    return inner


def field(parent, label):
    tk.Label(parent, text=label, font=(FONT, 10, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", pady=(8, 3))
    entry = tk.Entry(parent, font=(FONT, 11), relief="flat", bg="#F8FAF8",
                     fg=TEXT, insertbackground=TEXT,
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=PRIMARY)
    entry.pack(fill="x", ipady=6)
    return entry


def button(parent, text, command, primary=True, width=None, danger=False):
    bg = PRIMARY if primary else CARD
    fg = "white" if primary else PRIMARY
    hover = PRIMARY_HOVER if primary else "#E9EFEC"
    if danger:
        bg, fg, hover, primary = DANGER, "white", DANGER_HOVER, True
    b = tk.Button(parent, text=text, command=command,
                  font=(FONT, 10, "bold"), bg=bg, fg=fg,
                  activebackground=hover, activeforeground=fg,
                  relief="flat", bd=0, cursor="hand2",
                  highlightthickness=0 if primary else 1,
                  highlightbackground=BORDER, pady=9, padx=14)
    if width:
        b.config(width=width)
    b.bind("<Enter>", lambda e: b.config(bg=hover))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def combo(parent, label, values):
    tk.Label(parent, text=label, font=(FONT, 10, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", pady=(8, 3))
    box = ttk.Combobox(parent, values=values, font=(FONT, 11))
    box.pack(fill="x", ipady=4)
    return box


def finish(win, first, action):
    """Focus first field, Enter = main action, Esc = close, window stays on top."""
    win.bind("<Return>", lambda e: action())
    win.bind("<Escape>", lambda e: win.destroy())
    win.transient(win.master)

    def grab():
        try:
            win.grab_set()
        except tk.TclError:
            pass

    win.after(100, grab)
    first.focus_set()