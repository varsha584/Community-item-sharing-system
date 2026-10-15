import tkinter as tk
from tkinter import ttk

import theme
import data


def view_items(root):

    window = tk.Toplevel(root)
    theme.setup(window, "View Items", "1000x560")
    window.minsize(820, 400)
    theme.header(window, "All items", "Everything shared so far")

    rows = data.get_all_items()

    if len(rows) == 0:

        tk.Label(window, text="No items yet. Use Add item to share the first one.",
                 font=(theme.FONT, 11), bg=theme.BG,
                 fg=theme.MUTED).pack(pady=40)

        return

    style = ttk.Style(window)
    style.theme_use("clam")
    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
    style.configure("Treeview", background=theme.CARD,
                    fieldbackground=theme.CARD, foreground=theme.TEXT,
                    rowheight=38, font=(theme.FONT, 10), borderwidth=0)
    style.configure("Treeview.Heading", background=theme.PRIMARY,
                    foreground="white", font=(theme.FONT, 10, "bold"),
                    relief="flat", padding=(10, 10))
    style.map("Treeview.Heading", background=[("active", theme.PRIMARY_HOVER)])
    style.map("Treeview", background=[("selected", "#D5E6E2")],
              foreground=[("selected", theme.TEXT)])

    # (column, width, alignment, stretches when window grows)
    layout = [
        ("ID", 50, "center", False),
        ("Item", 170, "w", True),
        ("Category", 130, "w", True),
        ("Owner", 130, "w", True),
        ("Status", 100, "center", False),
        ("Borrower", 130, "w", True),
        ("Due date", 150, "center", False),
    ]

    columns = [c[0] for c in layout]

    outer = tk.Frame(window, bg=theme.BG)
    outer.pack(fill="both", expand=True, padx=24, pady=(18, 8))

    wrap = tk.Frame(outer, bg=theme.CARD,
                    highlightbackground=theme.BORDER, highlightthickness=1)
    wrap.pack(fill="both", expand=True)

    table = ttk.Treeview(wrap, columns=columns, show="headings")

    for name, width, anchor, stretch in layout:
        table.heading(name, text=name, anchor=anchor)
        table.column(name, width=width, minwidth=width,
                     anchor=anchor, stretch=stretch)

    table.tag_configure("odd", background="#F6F9F7")
    table.tag_configure("Available", foreground=theme.GREEN)
    table.tag_configure("Borrowed", foreground=theme.AMBER)
    table.tag_configure("Overdue", foreground=theme.DANGER,
                        background="#FBEAE7")

    available = 0
    borrowed = 0
    overdue = 0

    for i, row in enumerate(rows):

        borrower = row[6] if row[6] else "-"
        due = row[7] if len(row) > 7 and row[7] else "-"
        status = row[5]
        tag = row[5]

        if status == "Available":
            available += 1
        elif status == "Borrowed":
            borrowed += 1

            left = data.days_left(row[7] if len(row) > 7 else "")

            if left is not None and left < 0:
                overdue += 1
                status = "Overdue"
                tag = "Overdue"
                due = f"{due}  ({-left}d late)"

        table.insert(
            "", tk.END,
            values=(row[0], row[1], row[2], row[4], status, borrower, due),
            tags=(tag, "odd" if i % 2 else "")
        )

    scroll = ttk.Scrollbar(wrap, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scroll.set)

    scroll.pack(side="right", fill="y")
    table.pack(fill="both", expand=True)

    tk.Label(window,
             text=(f"{len(rows)} items   |   {available} available   |   "
                f"{borrowed} borrowed   |   {overdue} overdue"),
             font=(theme.FONT, 10), bg=theme.BG,
             fg=theme.MUTED).pack(anchor="w", padx=26, pady=(0, 14))