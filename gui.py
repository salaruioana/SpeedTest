# gui.py
import tkinter as tk
from speedtest_engine import run_speed_test
from dial import SpeedDial
from utils import bits_to_mbps

# Theme self.COLORS
THEMES = {
    "dark": {
        "bg": "#0a0f1f",
        "fg": "#00ffe0",
        "accent": "#ff4f00",
        "button_bg": "#1a1f30",
        "button_fg": "#ffffff",
    },
    "light": {
        "bg": "#f0f0f0",
        "fg": "#003366",
        "accent": "#ff9900",
        "button_bg": "#ffffff",
        "button_fg": "#000000",
    }
}


class SpeedTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Test Dashboard")
        self.widgets = []  # to keep track of all themeable widgets

        self.theme = "dark"  # default theme
        self.COLORS = THEMES[self.theme]
        self.root.configure(bg=self.COLORS["bg"])

        # Label
        self.title =tk.Label(
            root,
            text=" Speed Test ",
            font=("Consolas", 20, "bold"),
            bg=self.COLORS["bg"],
            fg=self.COLORS["fg"],
            padx =2,
            pady=10
            )
        self.title.pack()
        self.widgets.append(self.title)

        self.toggle_button = tk.Button(
            root,
            text="Switch Theme",
            font=("Consolas", 10, "bold"),
            bg=self.COLORS["button_bg"],
            fg=self.COLORS["button_fg"],
            activebackground=self.COLORS["accent"],
            activeforeground=self.COLORS["button_fg"],
            command=self.toggle_theme,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5
        )
        self.toggle_button.place(relx=1.0, x=-10, y=10, anchor="ne")
        self.widgets.append(self.toggle_button)
        self.root.bind("<Configure>", self.position_toggle_button)


        self.speed_var = tk.DoubleVar(value=0)

        self.download_label_var = tk.StringVar(value="Download: - Mbps")
        self.upload_label_var = tk.StringVar(value="Upload: - Mbps")
        self.ping_label_var = tk.StringVar(value="Ping: - ms")
        self.isp_label_var = tk.StringVar(value="ISP: -")
        self.server_label_var = tk.StringVar(value="Server: -")
        self.location_label_var = tk.StringVar(value="Location: -")

        # Speed Dial Widget
        self.dial = SpeedDial(root, max_speed=500)
        self.dial.pack(pady=20)

        # Speed Labels
        self.download_label = tk.Label(root, textvariable=self.download_label_var, font=("Consolas", 14),
                                       bg=self.COLORS["bg"], fg=self.COLORS["fg"])
        self.download_label.pack()
        self.widgets.append(self.download_label)

        self.upload_label = tk.Label(root, textvariable=self.upload_label_var, font=("Consolas", 14),
                                     bg=self.COLORS["bg"], fg=self.COLORS["fg"])
        self.upload_label.pack()
        self.widgets.append(self.upload_label)

        self.ping_label = tk.Label(root, textvariable=self.ping_label_var, font=("Consolas", 14),
                                     bg=self.COLORS["bg"], fg=self.COLORS["fg"])
        self.ping_label.pack()
        self.widgets.append(self.ping_label)

        self.isp_label = tk.Label(root, textvariable=self.isp_label_var, font=("Consolas", 14),
                                   bg=self.COLORS["bg"], fg=self.COLORS["fg"])
        self.isp_label.pack()
        self.widgets.append(self.isp_label)

        self.server_label = tk.Label(root, textvariable=self.server_label_var, font=("Consolas", 14),
                                   bg=self.COLORS["bg"], fg=self.COLORS["fg"])
        self.server_label.pack()
        self.widgets.append(self.server_label)

        self.location_label = tk.Label(root, textvariable=self.location_label_var, font=("Consolas", 14),
                                   bg=self.COLORS["bg"], fg=self.COLORS["fg"])
        self.location_label.pack()
        self.widgets.append(self.location_label)

        # Start Button
        self.start_button = tk.Button(
            root,
            text="Start Test",
            font=("Consolas", 12, "bold"),
            bg=self.COLORS["button_bg"],
            fg=self.COLORS["button_fg"],
            activebackground=self.COLORS["accent"],
            activeforeground=self.COLORS["button_fg"],
            command=self.run_test,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        self.start_button.pack(pady=30)
        self.widgets.append(self.start_button)

    def position_toggle_button(self, event):
        self.toggle_button.place(x=event.width - 120, y=10)

    def run_test(self):
        self.start_button.config(state="disabled", text="Testing...")
        self.dial.start_loading()
        self.root.after(5, self._run_speedtest_async)

    def _run_speedtest_async(self):
        import threading
        threading.Thread(target=self._do_speedtest, daemon=True).start()

    def _do_speedtest(self):
        results = run_speed_test()
        if "error" in results:
            self.download_label_var.set("Error: " + results["error"])
            self.upload_label_var.set("Upload: -")
            self.start_button.config(state="normal", text="Start Test")
            return
        download_mbps = bits_to_mbps(results["download"])
        upload_mbps = bits_to_mbps(results["upload"])
        ping_ms = results["ping"]
        isp = results["isp"]
        server = results["server"]
        location = results["location"]

        # Update GUI (back to main thread)
        self.root.after(0, self.update_results, download_mbps, upload_mbps,ping_ms,isp,server,location)

    def update_results(self, download, upload,ping,isp,server,location):
        self.dial.stop_loading()  # Stop the idle animation
        self.download_label_var.set(f"Download: {download}")
        self.upload_label_var.set(f"Upload: {upload}")
        self.ping_label_var.set(f"Ping: {ping}")
        self.isp_label_var.set(f"ISP: {isp}")
        self.server_label_var.set(f"Server: {server}")
        self.location_label_var.set(f"Location: {location}")
        self.dial.set_speed(download)

        self.start_button.config(state="normal", text="Start Test")

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.COLORS = THEMES[self.theme]
        self.root.configure(bg=self.COLORS["bg"])
        self.apply_theme()

    def apply_theme(self):
        # Update general window background
        self.root.configure(bg=self.COLORS["bg"])

        # Apply theme to all widgets
        for widget in self.widgets:
            if isinstance(widget, tk.Label):
                widget.configure(bg=self.COLORS["bg"], fg=self.COLORS["fg"])
            elif isinstance(widget, tk.Button):
                widget.configure(
                    bg=self.COLORS["button_bg"],
                    fg=self.COLORS["button_fg"],
                    activebackground=self.COLORS["accent"],
                    activeforeground=self.COLORS["button_fg"]
                )

        # Re-color the toggle button too
        self.toggle_button.configure(
            bg=self.COLORS["button_bg"],
            fg=self.COLORS["button_fg"],
            activebackground=self.COLORS["accent"],
            activeforeground=self.COLORS["button_fg"]
        )
