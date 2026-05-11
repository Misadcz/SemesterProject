import tkinter as tk
from tkinter import ttk
from pathlib import Path
from gui.slides.base_slide import BaseSlide


import subprocess

def import_virtualbox_ova(ova_path):
    vboxmanage_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
    
    try:
        subprocess.run(
            [vboxmanage_path, 'import', ova_path], 
            check=True, 
            capture_output=True, 
            text=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


class SlideVMImport(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 2: Environment Image Import", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        import_frame = ttk.LabelFrame(self, text=" VM Image (.ova) ", padding=(10, 5))
        import_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(import_frame, justify=tk.LEFT, text=(
            "The pre-configured development environment is provided as an .ova file.\n\n"
            "Instructions:\n"
            "1. Click 'Locate Image' to find the file in your 'libs' folder.\n"
            "2. In VirtualBox, go to 'File' -> 'Import Appliance'.\n"
            "3. Select the located file and follow the import wizard."
        )).pack(anchor=tk.W, pady=5)

        self.path_label = tk.Label(import_frame, text="Image Location: Not located yet", fg="blue", wraplength=450)
        self.path_label.pack(anchor=tk.W, pady=5)

        tk.Button(import_frame, text="📂 Locate Image in 'libs'", command=self.locate_image).pack(anchor=tk.W, pady=5)

        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def locate_image(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        image_file = list((base_dir / "libs").glob("*.ova"))
        if image_file:
            path = str(image_file[0])
            self.path_label.config(text=f"Image Location: {path}", fg="green")
            self.app.log_message(f"VM Image found: {image_file[0].name}")
        else:
            self.path_label.config(text="Error: No .ova file found in 'libs' folder!", fg="red")