import tkinter as tk
from tkinter import ttk
import webbrowser
import subprocess
import threading
import sys
import ctypes
from pathlib import Path
from gui.slides.base_slide import BaseSlide

class SlideVirtualization(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 1: Virtualization Environment", font=("Arial", 16, "bold")).pack(pady=(10, 5))

        vbox_frame = ttk.LabelFrame(self, text=" VirtualBox Installation ", padding=(10, 5))
        vbox_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(vbox_frame, justify=tk.LEFT, text=(
            "Download and install VirtualBox (if not already installed).\n"
        )).pack(anchor=tk.W, pady=(0, 5))
        
        btn_frame = tk.Frame(vbox_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        self.create_link_button(btn_frame, " Download VirtualBox", "https://www.virtualbox.org/wiki/Downloads", bg="#cce5ff")
        
        self.install_btn = tk.Button(vbox_frame, text="⚙️ Run Local Installer (VirtualBox-7.2.6a)", 
                                     font=("Arial", 9, "bold"), bg="#d4edda", command=self.run_local_vbox_installer)
        self.install_btn.pack(anchor=tk.W, pady=5)

        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 1: Ready to setup VirtualBox.")

    def run_local_vbox_installer(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        installer_path = base_dir / "libs" / "VirtualBox-7.2.6a-172322-Win.exe"
        
        if installer_path.exists():
            self.app.log_message(f"Launching VirtualBox installer: {installer_path.name}")
            try:
                if sys.platform == "win32":
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", str(installer_path), None, None, 1)
                else:
                    subprocess.Popen([str(installer_path)])
            except Exception as e:
                self.app.log_message(f"Error launching installer: {e}")
        else:
            self.app.log_message(f"File '{installer_path.name}' not found in 'libs' folder!")