# speed_dial.py
import tkinter as tk
import math

class SpeedDial(tk.Canvas):
    def __init__(self, parent, width=500, height=200, max_speed=1000, **kwargs):
        super().__init__(parent, width=width, height=height, bg="black", highlightthickness=0, **kwargs)

        self.width = width
        self.height = height
        self.max_speed = max_speed
        self.current_speed = 0
        self.target_speed = 0

        self.center_x = width // 2
        self.center_y = height
        self.radius = min(width, height)

        self.needle = None
        self.speed_text = None

        self.loading = False
        self._needle_direction = 1  # 1 = forward, -1 = backward

        self.create_dial()
        self.animate()

    def create_dial(self):
        # Arc for dial background
        self.create_arc(10, 10, self.width - 10, self.height * 2 - 10, start=180, extent=180,
                        style="arc", outline="#00ffe0", width=3)

        # Tick marks
        for i in range(0, 11):
            angle_deg = 180 + i * 18
            angle_rad = math.radians(angle_deg)
            x0 = self.center_x + (self.radius * 0.45) * math.cos(angle_rad)
            y0 = self.center_y + (self.radius * 0.45) * math.sin(angle_rad)
            x1 = self.center_x + (self.radius * 0.5) * math.cos(angle_rad)
            y1 = self.center_y + (self.radius * 0.5) * math.sin(angle_rad)
            self.create_line(x0, y0, x1, y1, fill="#ffffff")

        # Static text: Mbps
        self.create_text(self.center_x, self.center_y - 20, text="Mbps",
                         fill="#ffffff", font=("Consolas", 12, "bold"))

        # Initial needle and speed text
        self.needle = self.create_line(self.center_x, self.center_y,
                                       self.center_x, self.center_y - self.radius * 0.4,
                                       fill="#ff4f00", width=3)
        self.speed_text = self.create_text(self.center_x, self.center_y - 60,
                                           text="0", fill="#00ffe0",
                                           font=("Consolas", 20, "bold"))

    def set_speed(self, speed):
        # Clamp and set target speed
        self.target_speed = max(0, min(speed, self.max_speed))

    def animate(self):
        if self.loading:
            # Animate idle sweep between 0 and 500 Mbps
            if self.current_speed >= 500:
                self._needle_direction = -1
            elif self.current_speed <= 0:
                self._needle_direction = 1
            self.current_speed += self._needle_direction * 1
            self.after(70, self.animate)

        else:
            # Smoothly animate toward target
            if abs(self.current_speed - self.target_speed) > 1:
                self.current_speed += (self.target_speed - self.current_speed) * 0.1
            else:
                self.current_speed = self.target_speed
            self.after(20, self.animate)

        self.update_needle()

    def start_loading(self):
        self.loading = True

    def stop_loading(self):
        self.loading = False
        self.set_speed(0)

    def update_needle(self):
        angle = 180 + (self.current_speed / self.max_speed) * 180
        angle_rad = math.radians(angle)

        x = self.center_x + self.radius * 0.4 * math.cos(angle_rad)
        y = self.center_y + self.radius * 0.4 * math.sin(angle_rad)

        self.coords(self.needle, self.center_x, self.center_y, x, y)
        self.itemconfig(self.speed_text, text=f"{int(self.current_speed)}")
