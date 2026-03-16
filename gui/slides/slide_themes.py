import tkinter as tk
from tkinter import ttk
import threading
import zipfile
import shutil
from pathlib import Path
from gui.slides.base_slide import BaseSlide

class SlideThemes(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 3: Themes and Node.js / Gulp", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        tk.Label(self, text="Dependencies will be extracted from 'libs' into your Workspace repository.").pack(pady=(0, 10))

        # --- DRIVES COMPASS THEME SECTION ---
        compass_frame = ttk.LabelFrame(self, text=" 1. drives-compass-theme ", padding=(10, 5))
        compass_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(compass_frame, justify=tk.LEFT, text=(
            "Click below to automatically extract 'node_modules' and copy 'liferay-theme.json'\n"
            "into the drives-compass-theme folder in your Workspace."
        )).pack(anchor=tk.W, pady=(0, 5))

        self.compass_btn = tk.Button(compass_frame, text="📦 Setup drives-compass-theme", bg="#cce5ff", font=("Arial", 10, "bold"),
                                     command=self.setup_compass)
        self.compass_btn.pack(anchor=tk.W, pady=5, padx=5)

        tk.Label(compass_frame, font=("Arial", 9, "bold"), text="After setup, go to 'node_modules/.bin' and run: ./gulp deploy").pack(anchor=tk.W, pady=(5, 0))

        # --- MSK THEME SECTION ---
        msk_frame = ttk.LabelFrame(self, text=" 2. msk-theme ", padding=(10, 5))
        msk_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(msk_frame, justify=tk.LEFT, text=(
            "Click below to automatically extract 'msk-theme' and copy 'liferay-theme.json'\n"
            "into the wars folder in your Workspace."
        )).pack(anchor=tk.W, pady=(0, 5))

        self.msk_btn = tk.Button(msk_frame, text="📦 Setup msk-theme", bg="#cce5ff", font=("Arial", 10, "bold"),
                                 command=self.setup_msk)
        self.msk_btn.pack(anchor=tk.W, pady=5, padx=5)

        tk.Label(msk_frame, font=("Arial", 9, "bold"), text="After setup, go to 'node_modules/.bin' and run: ./gulp deploy").pack(anchor=tk.W, pady=(5, 0))

        # --- NAVIGATION ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 3: Ready to extract theme dependencies.")

    # --- COMPASS THEME METHODS ---
    def setup_compass(self):
        self.compass_btn.config(text="⏳ Setting up drives-compass-theme (Please wait)...", state=tk.DISABLED, bg="#f8d7da")
        self.app.log_message("Starting background extraction for drives-compass-theme...")

        thread = threading.Thread(target=self._run_compass_setup)
        thread.daemon = True
        thread.start()

    def _run_compass_setup(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        libs_dir = base_dir / "libs"
        
        # Cílová cesta ve Workspace repozitáři
        target_dir = base_dir / "Workspace" / "platform" / "eu.project-drives.platform" / "wars" / "drives-compass-theme"
        zip_path = libs_dir / "node_modules.zip"
        json_path = libs_dir / "liferay-theme.json"

        if not zip_path.exists():
            self.app.after(0, self._on_compass_error, f"File {zip_path.name} not found in 'libs'!")
            return

        try:
            # Vytvoření cílové složky, pokud repozitář ještě nebyl naklonován
            target_dir.mkdir(parents=True, exist_ok=True)

            # Rozbalení node_modules.zip
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)

            # Zkopírování liferay-theme.json
            if json_path.exists():
                shutil.copy(json_path, target_dir / "liferay-theme.json")

            self.app.after(0, self._on_compass_success)
        except Exception as e:
            self.app.after(0, self._on_compass_error, str(e))

    def _on_compass_success(self):
        self.compass_btn.config(text="✔ drives-compass-theme setup complete", bg="#d4edda")
        self.app.log_message("node_modules and liferay-theme.json were successfully copied to drives-compass-theme.")

    def _on_compass_error(self, error_msg):
        self.compass_btn.config(text="❌ Error (Try again)", state=tk.NORMAL, bg="#f5c6cb")
        self.app.log_message(f"ERROR: {error_msg}")

    # --- MSK THEME METHODS ---
    def setup_msk(self):
        self.msk_btn.config(text="⏳ Setting up msk-theme (Please wait)...", state=tk.DISABLED, bg="#f8d7da")
        self.app.log_message("Starting background extraction for msk-theme...")

        thread = threading.Thread(target=self._run_msk_setup)
        thread.daemon = True
        thread.start()

    def _run_msk_setup(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        libs_dir = base_dir / "libs"
        
        # Cílová cesta pro složku wars
        wars_dir = base_dir / "Workspace" / "platform" / "eu.project-drives.platform" / "wars"
        zip_path = libs_dir / "msk-theme.zip"
        json_path = libs_dir / "liferay-theme.json"

        if not zip_path.exists():
            self.app.after(0, self._on_msk_error, f"File {zip_path.name} not found in 'libs'!")
            return

        try:
            # Vytvoření cílové složky
            wars_dir.mkdir(parents=True, exist_ok=True)

            # Rozbalení celého msk-theme.zip do složky wars
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(wars_dir)

            # Zkopírování liferay-theme.json do nové složky msk-theme
            msk_theme_dir = wars_dir / "msk-theme"
            msk_theme_dir.mkdir(parents=True, exist_ok=True)
            
            if json_path.exists():
                shutil.copy(json_path, msk_theme_dir / "liferay-theme.json")

            self.app.after(0, self._on_msk_success)
        except Exception as e:
            self.app.after(0, self._on_msk_error, str(e))

    def _on_msk_success(self):
        self.msk_btn.config(text="✔ msk-theme setup complete", bg="#d4edda")
        self.app.log_message("msk-theme was successfully extracted and configured.")

    def _on_msk_error(self, error_msg):
        self.msk_btn.config(text="❌ Error (Try again)", state=tk.NORMAL, bg="#f5c6cb")
        self.app.log_message(f"ERROR: {error_msg}")