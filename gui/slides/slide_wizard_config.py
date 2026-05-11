import tkinter as tk
from tkinter import ttk
from gui.slides.base_slide import BaseSlide

class SlideWizardConfig(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 4: VM Configuration", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        tk.Label(self, text="Configure your Liferay portal access inside the Virtual Machine.").pack(pady=(0, 10))

        config_frame = ttk.LabelFrame(self, text=" Edit portal-setup-wizard.properties ", padding=(10, 5))
        config_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(config_frame, justify=tk.LEFT, text=(
            "1. Start your imported Virtual Machine in VirtualBox.\n"
            "2. Inside the VM, open a text editor (e.g., Nano, Gedit, or VS Code).\n"
            "3. Open the file located at the path below:\n"
        )).pack(anchor=tk.W, pady=(0, 5))
        
        path_text = tk.Text(config_frame, height=2, bg="#f0f0f0", font=("Consolas", 10))
        path_text.insert(tk.END, "/home/guest/project/workspace/liferay-ce-portal-7.3.3-ga4/\nportal-setup-wizard.properties")
        path_text.config(state=tk.DISABLED) 
        path_text.pack(fill=tk.X, pady=5, padx=5)

        tk.Label(config_frame, justify=tk.LEFT, text=(
            "4. Find the login configuration line.\n"
            "5. Replace it with your actual login credentials and save the file."
        )).pack(anchor=tk.W, pady=(5, 0))

        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 4: Displayed VM configuration instructions.")