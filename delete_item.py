import tkinter as tk
from tkinter import messagebox

import theme
import data


def delete_item(root):

    window = tk.Toplevel(root)
    theme.setup(window, "Delete Item", "460x560")
    theme.header(window, "Delete item", "Remove an item permanently")

    form = theme.card(window)

    id_entry = theme.field(form, "Item ID")

    loaded = {"id": None}

    details = tk.Label(form, text="Item details will appear here.",
                       font=(theme.FONT, 10), justify="left", anchor="nw",
                       bg="#F8FAF8", fg=theme.MUTED,
                       highlightbackground=theme.BORDER,
                       highlightthickness=1)

    def read_id():

        entered_id = id_entry.get().strip()

        if entered_id == "":
            messagebox.showwarning("Warning", "Please enter Item ID.")
            return None

        if not entered_id.isdigit():
            messagebox.showwarning("Warning", "Item ID must be a number.")
            return None

        return int(entered_id)

    def load():

        item_id = read_id()

        if item_id is None:
            return

        item = data.get_item(item_id)

        if item is None:
            loaded["id"] = None
            messagebox.showerror("Error", "Item ID not found.")
            return

        loaded["id"] = item[0]

        borrower = item[6] if item[6] != "" else "None"

        details.config(
            text=(
                f"Name:  {item[1]}\n\n"
                f"Category:  {item[2]}\n\n"
                f"Owner:  {item[4]}\n\n"
                f"Status:  {item[5]}\n\n"
                f"Borrower:  {borrower}"
            ),
            fg=theme.TEXT,
            font=(theme.FONT, 11),
            padx=14, pady=12
        )

    theme.button(form, "Load item", load, False).pack(
        fill="x", pady=(10, 12))

    details.pack(fill="both", expand=True)

    def delete():

        if loaded["id"] is None:
            messagebox.showwarning(
                "Warning", "Load an item first using its Item ID.")
            return

        item = data.get_item(loaded["id"])

        if item is None:
            messagebox.showerror("Error", "Item no longer exists.")
            return

        if item[5] == "Borrowed":
            messagebox.showwarning(
                "Cannot delete",
                f"{item[1]} is borrowed by {item[6]}.\n"
                "Return it before deleting."
            )
            return

        if not messagebox.askyesno(
            "Confirm delete",
            f"Delete {item[1]} permanently?\nThis cannot be undone."
        ):
            return

        if data.delete_item(loaded["id"]) == 1:

            messagebox.showinfo("Success", f"{item[1]} deleted.")

            window.destroy()

        else:

            messagebox.showerror("Error", "Item could not be deleted.")

    theme.button(form, "Delete item", delete, danger=True).pack(
        fill="x", pady=(16, 0))

    # Enter only loads the item; deleting always needs the button + confirmation
    theme.finish(window, id_entry, load)