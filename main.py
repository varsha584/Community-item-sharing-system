import tkinter as tk

import theme
from dashboard import show_dashboard


root = tk.Tk()

theme.setup(root, "ShareHub", "560x720")

show_dashboard(root)

root.mainloop()