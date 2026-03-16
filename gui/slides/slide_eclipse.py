import tkinter as tk
from tkinter import ttk
import os
import sys
import subprocess
import threading
from pathlib import Path
from gui.slides.base_slide import BaseSlide

class SlideEclipse(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 4: Eclipse Installation and Configuration", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        # --- ECLIPSE IDE SECTION ---
        eclipse_frame = ttk.LabelFrame(self, text=" 1. Eclipse IDE (2020-06) ", padding=(10, 5))
        eclipse_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(eclipse_frame, justify=tk.LEFT, text=(
            "Run the included Eclipse installer and follow these steps:\n"
            "1. Select 'Eclipse IDE for Enterprise Java Developers'.\n"
            "2. Complete the installation and close the installer.\n"
            "IMPORTANT: After installation, find eclipse.ini and set the Java path in it (min. version 17!)."
        )).pack(anchor=tk.W, pady=(0, 5))

        btn_frame = tk.Frame(eclipse_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Button for offline installation
        self.install_btn = tk.Button(btn_frame, text="⚙️ Run Eclipse Installation", 
                                     font=("Arial", 10, "bold"), bg="#d4edda", 
                                     command=self.start_installation)
        self.install_btn.pack(side=tk.LEFT, padx=5)

        # --- LIFERAY PLUGIN SECTION (VIDEO) ---
        plugin_frame = ttk.LabelFrame(self, text=" 2. Liferay Eclipse plugin ", padding=(10, 5))
        plugin_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(plugin_frame, text="Guide: Liferay plugin installation via Eclipse Marketplace").pack(anchor=tk.W, pady=(0, 5))

        # Play video button
        play_btn = tk.Button(plugin_frame, text="▶ Open Video Guide", font=("Arial", 10, "bold"), bg="#cce5ff", command=self.play_video)
        play_btn.pack(anchor=tk.W, pady=10, padx=5)

        # --- NAVIGATION ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=10)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 4: Displayed instructions for local Eclipse installation.")

    # --- INSTALLATION METHODS ---
    def start_installation(self):
        """Starts the installation process in a new thread."""
        self.install_btn.config(text="⏳ Installer is running...", state=tk.DISABLED, bg="#f8d7da")
        self.app.log_message("Starting Eclipse installer. Please complete the setup in the new window.")

        # Run in thread
        install_thread = threading.Thread(target=self._run_installer_in_background)
        install_thread.daemon = True 
        install_thread.start()

    def _run_installer_in_background(self):
        """Runs in background and waits for the installation to finish."""
        base_dir = Path(__file__).resolve().parent.parent.parent
        installer_path = base_dir / "libs" / "eclipse-inst-win64 (202-06 R).exe"

        if not installer_path.exists():
            self.app.after(0, self._on_install_error, f"File not found: {installer_path.name}")
            return

        try:
            # subprocess.run waits for the program to close
            subprocess.run([str(installer_path)], check=True)
            self.app.after(0, self._on_install_success)
        except Exception as e:
            self.app.after(0, self._on_install_error, str(e))

    def _on_install_success(self):
        """Called from the main thread after the installer is closed."""
        self.install_btn.config(text="✔ Installation process finished", bg="#d4edda", state=tk.NORMAL)
        self.app.log_message("Eclipse installer was closed.")

    def _on_install_error(self, error_msg):
        """Called from the main thread in case of an error."""
        self.install_btn.config(text="❌ Error (Try again)", bg="#f5c6cb", state=tk.NORMAL)
        self.app.log_message(f"ERROR launching installer: {error_msg}")

    # --- VIDEO METHOD ---
    def play_video(self):
        """Opens the video guide in the default system player."""
        base_dir = Path(__file__).resolve().parent.parent.parent
        video_path = base_dir / "assets" / "liferay_in_eclipse_1.mp4"

        if not video_path.exists():
            self.app.log_message(f"ERROR: Video not found at path: {video_path}")
            return

        try:
            self.app.log_message(f"Playing video: {video_path.name}")
            if sys.platform == "win32":
                os.startfile(video_path)
            elif sys.platform == "darwin":  
                subprocess.call(["open", str(video_path)])
            else:  
                subprocess.call(["xdg-open", str(video_path)])
        except Exception as e:
            self.app.log_message(f"Error playing video: {e}")