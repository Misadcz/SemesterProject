import tkinter as tk
from tkinter import ttk
from gui.slides.base_slide import BaseSlide

class SlideGulpDeploy(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 5: Initial Theme Deployment", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        tk.Label(self, text="Deploy the base theme components inside the Virtual Machine.").pack(pady=(0, 10))

        deploy_frame = ttk.LabelFrame(self, text=" Run Gulp Deploy ", padding=(10, 5))
        deploy_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(deploy_frame, justify=tk.LEFT, text=(
            "1. In your VM, open a Terminal (usually Ctrl+Alt+T).\n"
            "2. Navigate to the '.bin' directory using the following path:\n"
        )).pack(anchor=tk.W, pady=(0, 5))
        
        path_text = tk.Text(deploy_frame, height=2, bg="#f0f0f0", font=("Consolas", 10))
        path_text.insert(tk.END, "/home/guest/project/workspace/liferay-ce-portal-7.3.3-ga4/.bin/")
        path_text.config(state=tk.DISABLED)
        path_text.pack(fill=tk.X, pady=5, padx=5)

        tk.Label(deploy_frame, justify=tk.LEFT, text=(
            "3. Run the deployment command:\n"
        )).pack(anchor=tk.W, pady=(5, 0))

        cmd_text = tk.Text(deploy_frame, height=1, bg="#2d2d2d", fg="#61afef", font=("Consolas", 10, "bold"))
        cmd_text.insert(tk.END, "./gulp deploy")
        cmd_text.config(state=tk.DISABLED)
        cmd_text.pack(fill=tk.X, pady=5, padx=5)

        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 5: Gulp deployment instructions displayed.")