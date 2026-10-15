import tkinter as tk
from tkinter import messagebox

import theme
import data


def return_item(root):

    window = tk.Toplevel(root)
    theme.setup(window, "Return Item", "440x380")
    theme.header(window, "Return item", "Mark a borrowed item as available")

    form = theme.card(window)

    id_entry = theme.field(form, "Item ID")

    def return_item_function():

        entered_id = id_entry.get().strip()

        if entered_id == "":
            messagebox.showwarning("Warning", "Please enter Item ID.")
            return

        if not entered_id.isdigit():
            messagebox.showwarning("Warning", "Item ID must be a number.")
            return

        item_id = int(entered_id)

        item = data.get_item(item_id)

        if item is None:
            messagebox.showerror("Error", "Item ID not found.")
            return

        if item[5] != "Borrowed":
            messagebox.showwarning(
                "Error", "This item is not currently borrowed.")
            return

        borrower_name = item[6]

        left = data.days_left(item[7] if len(item) > 7 else "")

        if left is None:
            timing = ""
        elif left < 0:
            timing = f"\nReturned {-left} day(s) late."
        elif left == 0:
            timing = "\nReturned on the due date."
        else:
            timing = f"\nReturned {left} day(s) early."

        changed = data.return_item(item_id)

        if changed == 1:

            messagebox.showinfo(
                "Success",
                f"{item[1]} returned successfully.\n"
                f"Borrower: {borrower_name}"
                f"{timing}"
            )

            window.destroy()

    theme.button(form, "Return", return_item_function).pack(
        fill="x", pady=(22, 0))

    theme.finish(window, id_entry, return_item_function)