import tkinter as tk
from tkinter import ttk
import webbrowser
from gui.slides.base_slide import BaseSlide

class SlideAccess(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 3: Access and Credentials", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        velart_frame = ttk.LabelFrame(self, text=" 1. GitLab Access (Zdeněk Velart) ", padding=(10, 5))
        velart_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(velart_frame, justify=tk.LEFT, text=(
            "To clone the project repository inside the VM, you need GitLab access.\n"
            "An automated email template has been prepared for you."
        )).pack(anchor=tk.W, pady=5)

        tk.Button(velart_frame, text="📧 Prepare Email to Ing. Velart", 
                  bg="#d4edda", command=self.open_email).pack(anchor=tk.W, pady=5)

        clone_frame = ttk.LabelFrame(self, text=" 2. SSH Key & Git Clone ", padding=(10, 5))
        clone_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(clone_frame, justify=tk.LEFT, text="Once your access is granted, log in to GitLab:").pack(anchor=tk.W)

        link_lbl = tk.Label(clone_frame, text="🔗 https://git.scoveco.cz/drives/platform", fg="blue", cursor="hand2")
        link_lbl.pack(anchor=tk.W, pady=(0, 10))
        link_lbl.bind("<Button-1>", lambda e: webbrowser.open("https://git.scoveco.cz/drives/platform"))

        instructions = (
            "• Click the 'Code' button and copy the 'Clone with SSH' URL.\n\n"
            "• NO SSH KEY? If you haven't added an SSH key to GitLab yet:\n"
            "  1. Click the warning/link above the clone URL to add a new key.\n"
            "  2. Open your Linux terminal and print your public key (e.g., run: cat ~/.ssh/id_rsa.pub).\n"
            "  3. Copy the output and paste it into GitLab.\n\n"
            "• Finally, open your terminal in the target workspace folder and run:\n"
            "  git clone <paste_your_copied_url_here>"
        )
        tk.Label(clone_frame, justify=tk.LEFT, text=instructions).pack(anchor=tk.W, pady=5)

        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def open_email(self):
        subject = "SkillsHub - Request for GitLab Access"
        body = "Hello,\n\nI am a new developer on the SkillsHub project and I would like to request access to the GitLab repository.\n\nThank you. My login is ABC1234."
        webbrowser.open(f"mailto:zdenek.velart@vsb.cz?subject={subject}&body={body}")