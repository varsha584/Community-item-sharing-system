import tkinter as tk
from tkinter import messagebox

import theme
import data


def borrow_item(root):

    window = tk.Toplevel(root)
    theme.setup(window, "Borrow Item", "440x580")
    theme.header(window, "Borrow item", "Take an available item")

    form = theme.card(window)

    id_entry = theme.field(form, "Item ID")
    borrower_entry = theme.field(form, "Borrower name")
    days_entry = theme.field(form, "Borrow duration (days)")
    days_entry.insert(0, "7")

    def borrow():

        entered_id = id_entry.get().strip()
        borrower_name = borrower_entry.get().strip()
        entered_days = days_entry.get().strip()

        if entered_id == "":
            messagebox.showwarning("Warning", "Please enter Item ID.")
            return

        if not entered_id.isdigit():
            messagebox.showwarning("Warning", "Item ID must be a number.")
            return

        if borrower_name == "":
            messagebox.showwarning("Warning", "Please enter borrower name.")
            return

        if (not entered_days.isdecimal()
                or not 1 <= int(entered_days) <= 365):
            messagebox.showwarning(
                "Warning",
                "Duration must be a whole number of days (1 to 365)."
            )
            return

        item_id = int(entered_id)
        days = int(entered_days)

        item = data.get_item(item_id)

        if item is None:
            messagebox.showerror("Error", "Item ID not found.")
            return

        if item[5] != "Available":
            messagebox.showwarning(
                "Unavailable", "This item is already borrowed.")
            return

        changed = data.borrow_item(item_id, borrower_name, days)

        if changed == 1:

            due_date = data.get_item(item_id)[7]

            messagebox.showinfo(
                "Success",
                f"{item[1]} borrowed successfully.\n"
                f"Borrower: {borrower_name}\n"
                f"Duration: {days} day(s)\n"
                f"Return by: {due_date}"
            )

            window.destroy()

    theme.button(form, "Borrow", borrow).pack(fill="x", pady=(22, 0))

    theme.finish(window, id_entry, borrow)