import tkinter as tk
from gui.slides.base_slide import BaseSlide

class SlideWelcome(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Welcome to SkillsHub Setup", font=("Arial", 18, "bold")).grid(row=0, column=0, pady=(40, 10))
        tk.Label(self, text="This tool will guide you through setting up your local development environment.\nThe process includes getting access, and installing Java, Liferay, and Node.js.").grid(row=1, column=0, pady=10)

        # Navigation buttons
        nav_frame = tk.Frame(self)
        nav_frame.grid(row=2, column=0, pady=30)
        tk.Button(nav_frame, text="Start ->", width=15, command=lambda: self.app.next_slide()).pack()

    def on_show(self):
        self.app.log_message("Guide started. Waiting for user action.")