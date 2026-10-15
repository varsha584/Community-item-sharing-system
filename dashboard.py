import tkinter as tk

import theme
import data
from add_item import add_item
from view_items import view_items
from search_item import search_item
from borrow_item import borrow_item
from return_item import return_item
from update_item import update_item
from delete_item import delete_item


def show_dashboard(root):

    theme.header(root, "ShareHub", "Borrow and lend within your community")

    body = tk.Frame(root, bg=theme.BG)
    body.pack(fill="both", expand=True, padx=24, pady=18)

    stats = tk.Frame(body, bg=theme.BG)
    stats.pack(fill="x")

    value_labels = {}

    for col, (key, title, color) in enumerate([
        ("total", "Total items", theme.PRIMARY),
        ("available", "Available", theme.GREEN),
        ("borrowed", "Borrowed", theme.AMBER),
        ("overdue", "Overdue", theme.DANGER),
    ]):
        stats.columnconfigure(col, weight=1, uniform="stat")

        box = tk.Frame(stats, bg=theme.CARD,
                       highlightbackground=theme.BORDER,
                       highlightthickness=1)
        box.grid(row=0, column=col, padx=5, sticky="nsew")

        value = tk.Label(box, text="0", font=(theme.FONT, 26, "bold"),
                         bg=theme.CARD, fg=color)
        value.pack(pady=(12, 0))

        tk.Label(box, text=title, font=(theme.FONT, 10),
                 bg=theme.CARD, fg=theme.MUTED).pack(pady=(0, 12))

        value_labels[key] = value

    def update_statistics():

        total, available, borrowed = data.get_statistics()

        value_labels["total"].config(text=str(total))
        value_labels["available"].config(text=str(available))
        value_labels["borrowed"].config(text=str(borrowed))
        value_labels["overdue"].config(text=str(data.get_overdue_count()))

        root.after(500, update_statistics)

    update_statistics()

    tk.Label(body, text="What would you like to do?",
             font=(theme.FONT, 12, "bold"),
             bg=theme.BG, fg=theme.TEXT).pack(anchor="w", pady=(24, 8))

    grid = tk.Frame(body, bg=theme.BG)
    grid.pack(fill="x")
    grid.columnconfigure(0, weight=1, uniform="a")
    grid.columnconfigure(1, weight=1, uniform="a")

    actions = [
        ("Add item", add_item, True),
        ("View items", view_items, False),
        ("Search item", search_item, False),
        ("Update item", update_item, False),
        ("Borrow item", borrow_item, True),
        ("Return item", return_item, False),
        ("Delete item", delete_item, False),
    ]

    for i, (text, func, primary) in enumerate(actions):
        theme.button(
            grid, text, lambda f=func: f(root), primary,
            danger=(text == "Delete item")
        ).grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="ew")

    theme.button(
        grid, "Exit", root.destroy, False
    ).grid(row=3, column=1, padx=5, pady=5, sticky="ew")