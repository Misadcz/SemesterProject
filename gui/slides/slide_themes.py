import tkinter as tk
from tkinter import ttk
from gui.slides.base_slide import BaseSlide

class SlideThemes(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 3: Themes and Node.js / Gulp", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        tk.Label(self, text="Download dependencies and compile CSS for each theme.").pack(pady=(0, 10))

        # --- DRIVES COMPASS THEME SECTION ---
        compass_frame = ttk.LabelFrame(self, text=" 1. drives-compass-theme ", padding=(10, 5))
        compass_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(compass_frame, justify=tk.LEFT, text=(
            "1. Download and extract 'node_modules' into the repository folder:\n"
            "   .../platform/eu.project-drives.platform/wars/drives-compass-theme\n"
            "2. Download 'liferay-theme.json', place it in the same folder and edit\n"
            "   the path to your Liferay portal in it."
        )).pack(anchor=tk.W, pady=(0, 5))

        btn_frame1 = tk.Frame(compass_frame)
        btn_frame1.pack(fill=tk.X, pady=5)
        
        self.create_link_button(btn_frame1, "Download node_modules.zip", "https://cybercloud.vsb.cz/index.php/f/100942", bg="#d4edda")
        self.create_link_button(btn_frame1, "Download liferay-theme.json", "https://cybercloud.vsb.cz/index.php/f/100943")

        tk.Label(compass_frame, font=("Arial", 9, "bold"), text="In the 'node_modules/.bin' folder, run the command: ./gulp deploy").pack(anchor=tk.W, pady=(5, 0))
        tk.Label(compass_frame, text="* Note: Run this command every time you change CSS or module design.", fg="#555555").pack(anchor=tk.W, pady=(0, 5))

        # --- MSK THEME SECTION ---
        msk_frame = ttk.LabelFrame(self, text=" 2. msk-theme (TODO) ", padding=(10, 5))
        msk_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(msk_frame, justify=tk.LEFT, text=(
            "1. Download the entire 'msk-theme' folder, extract it, and replace the existing folder in:\n"
            "   .../platform/eu.project-drives.platform/wars/msk-theme\n"
            "   (The provided zipped version has the Node.js issue resolved unlike the one in the repo).\n"
            "2. Find 'liferay-theme.json' inside it and again edit the path to the Liferay portal."
        )).pack(anchor=tk.W, pady=(0, 5))

        tk.Label(msk_frame, font=("Arial", 9, "bold"), text="In the 'node_modules/.bin' folder, run the command: ./gulp deploy").pack(anchor=tk.W, pady=(5, 0))
        tk.Label(msk_frame, text="* Note: Run this command every time you change CSS or module design.", fg="#555555").pack(anchor=tk.W, pady=(0, 5))

        # --- NAVIGATION ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 3: Displayed instructions and links for Gulp and themes.")