# main.py
import tkinter as tk
from gui import SpeedTestGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTestGUI(root)
    root.mainloop()
