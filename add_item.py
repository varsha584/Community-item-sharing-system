import tkinter as tk
from tkinter import messagebox

import theme
import data


def add_item(root):

    window = tk.Toplevel(root)
    theme.setup(window, "Add Item", "460x560")
    theme.header(window, "Add item", "Share something with the community")

    form = theme.card(window)

    name_entry = theme.field(form, "Item name")
    category_entry = theme.combo(form, "Category", theme.CATEGORIES)
    description_entry = theme.field(form, "Description (optional)")
    owner_entry = theme.field(form, "Owner")

    def save_item():

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

        item_id = data.add_item(name, category, description, owner)

        messagebox.showinfo(
            "Success",
            f"Item added successfully.\nItem ID: {item_id}"
        )

        window.destroy()

    theme.button(form, "Add item", save_item).pack(
        fill="x", pady=(22, 0))

    theme.finish(window, name_entry, save_item)