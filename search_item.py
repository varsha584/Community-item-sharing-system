import tkinter as tk
from tkinter import ttk, messagebox

import theme
import data


def search_item(root):

    window = tk.Toplevel(root)
    theme.setup(window, "Search Item", "520x680")
    theme.header(window, "Search item", "Look up details and availability")

    rows = data.get_all_items()

    if len(rows) == 0:

        tk.Label(window, text="No items yet. Use Add item to share the first one.",
                 font=(theme.FONT, 11), bg=theme.BG,
                 fg=theme.MUTED).pack(pady=40)

        return

    form = theme.card(window)

    tk.Label(form, text="Select an item", font=(theme.FONT, 10, "bold"),
             bg=theme.CARD, fg=theme.TEXT).pack(anchor="w", pady=(0, 3))

    item_list = [f"{r[0]} - {r[1]} - {r[5]}" for r in rows]

    selected_item = tk.StringVar()

    dropdown = ttk.Combobox(form, textvariable=selected_item,
                            values=item_list, state="readonly",
                            font=(theme.FONT, 11))
    dropdown.pack(fill="x", ipady=4)

    theme.button(form, "Search", lambda: search()).pack(
        fill="x", pady=(14, 14))

    result_frame = tk.Frame(form, bg="#F8FAF8",
                            highlightbackground=theme.BORDER,
                            highlightthickness=1)
    result_frame.pack(fill="both", expand=True)

    result_label = tk.Label(result_frame, text="Details will appear here.",
                            font=(theme.FONT, 10), justify="left",
                            anchor="nw", bg="#F8FAF8", fg=theme.MUTED)
    result_label.pack(fill="both", expand=True, padx=16, pady=14)

    def search():

        selected = selected_item.get()

        if selected == "":
            messagebox.showwarning("Warning", "Please select an item.")
            return

        item_id = int(selected.split(" - ")[0])

        item = data.get_item(item_id)

        if item is None:
            messagebox.showerror("Error", "Item not found.")
            return

        borrower = item[6] if item[6] != "" else "None"
        due = item[7] if item[7] else "None"

        left = data.days_left(item[7])

        if item[5] == "Borrowed" and left is not None and left < 0:
            due += f"  (overdue by {-left} day(s))"

        result = (
            f"Item ID:  {item[0]}\n\n"
            f"Name:  {item[1]}\n\n"
            f"Category:  {item[2]}\n\n"
            f"Description:  {item[3]}\n\n"
            f"Owner:  {item[4]}\n\n"
            f"Status:  {item[5]}\n\n"
            f"Borrower:  {borrower}\n\n"
            f"Due date:  {due}"
        )

        result_label.config(text=result, fg=theme.TEXT,
                            font=(theme.FONT, 11))