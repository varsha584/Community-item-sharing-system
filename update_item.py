import tkinter as tk
from tkinter import messagebox

import theme
import data


def update_item(root):

    window = tk.Toplevel(root)
    theme.setup(window, "Update Item", "460x700")
    theme.header(window, "Update item", "Edit the details of an item")

    form = theme.card(window)

    id_entry = theme.field(form, "Item ID")

    loaded = {"id": None}

    name_entry = None

    def fill(entry, value):
        entry.delete(0, tk.END)
        entry.insert(0, value or "")

    def load():

        entered_id = id_entry.get().strip()

        if entered_id == "":
            messagebox.showwarning("Warning", "Please enter Item ID.")
            return

        if not entered_id.isdigit():
            messagebox.showwarning("Warning", "Item ID must be a number.")
            return

        item = data.get_item(int(entered_id))

        if item is None:
            messagebox.showerror("Error", "Item ID not found.")
            return

        loaded["id"] = item[0]

        fill(name_entry, item[1])
        fill(category_entry, item[2])
        fill(description_entry, item[3])
        fill(owner_entry, item[4])

    theme.button(form, "Load item", load, False).pack(
        fill="x", pady=(10, 4))

    name_entry = theme.field(form, "Item name")
    category_entry = theme.combo(form, "Category", theme.CATEGORIES)
    description_entry = theme.field(form, "Description (optional)")
    owner_entry = theme.field(form, "Owner")

    def save():

        if loaded["id"] is None:
            messagebox.showwarning(
                "Warning", "Load an item first using its Item ID.")
            return

        name = name_entry.get().strip()
        category = category_entry.get().strip()
        description = description_entry.get().strip()
        owner = owner_entry.get().strip()

        if name == "":
            messagebox.showwarning("Warning", "Please enter item name.")
            return

        if category == "":
            messagebox.showwarning("Warning", "Please enter category.")
            return

        if owner == "":
            messagebox.showwarning("Warning", "Please enter owner name.")
            return

        changed = data.update_item(
            loaded["id"], name, category, description, owner)

        if changed == 1:

            messagebox.showinfo(
                "Success", f"{name} updated successfully.")

            window.destroy()

        else:

            messagebox.showerror("Error", "Item could not be updated.")

    theme.button(form, "Save changes", save).pack(fill="x", pady=(22, 0))

    theme.finish(window, id_entry,
                 lambda: save() if loaded["id"] else load())