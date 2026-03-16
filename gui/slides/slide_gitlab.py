import tkinter as tk
from tkinter import ttk
import webbrowser
import urllib.parse
from gui.slides.base_slide import BaseSlide

class SlideGitLab(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 1: GitLab Account and Cloning", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        # --- GITLAB ACCOUNT SECTION ---
        gitlab_frame = ttk.LabelFrame(self, text=" 1. GitLab Account Request ", padding=(10, 5))
        gitlab_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(gitlab_frame, justify=tk.LEFT, text=(
            "• To create a GitLab account, you must contact Zdeněk Velart.\n"
            "• You can request this via the form below, which will automatically pre-fill an email.\n"
            "• WARNING: After receiving the email from GitLab, you must set your password within 2 days!\n"
            "• If you miss this window, use the password reset link in the email."
        )).pack(anchor=tk.W)

        form_frame = tk.Frame(gitlab_frame)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Your full name:").grid(row=0, column=0, pady=5, sticky=tk.E)
        self.entry_name = tk.Entry(form_frame, width=35)
        self.entry_name.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Your school email:").grid(row=1, column=0, pady=5, sticky=tk.E)
        self.entry_email = tk.Entry(form_frame, width=35)
        self.entry_email.grid(row=1, column=1, pady=5, padx=10)

        tk.Button(gitlab_frame, text="✉ Generate and open email", bg="#d4edda", font=("Arial", 10, "bold"), 
                  command=self.create_email).pack(pady=5)

        # --- REPOSITORY CLONING SECTION ---
        clone_frame = ttk.LabelFrame(self, text=" 2. Cloning the repository ", padding=(10, 5))
        clone_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(clone_frame, justify=tk.LEFT, text=(
            "• Clone the Git repository into a local folder where you want to keep the project.\n"
            "• Make sure you have access rights and configured authentication\n"
            "  (e.g., SSH key or Personal Access Token) to pull and push changes."
        )).pack(anchor=tk.W, pady=(0, 5))

        btn_frame = tk.Frame(clone_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Button for repository link
        self.create_link_button(btn_frame, "Copy / Open link to repository", "https://git.scoveco.cz/drives/platform", bg="#cce5ff")

        # --- NAVIGATION ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=10)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 1: GitLab request and cloning instructions.")
        
        self.entry_name.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        
        self.entry_name.insert(0, self.app.state_manager.get("user", "name", ""))
        self.entry_email.insert(0, self.app.state_manager.get("user", "email", ""))

    def create_email(self):
        name = self.entry_name.get().strip()
        email = self.entry_email.get().strip()

        if not name or not email:
            self.app.log_message("ERROR: Please fill in both name and email.")
            return

        self.app.state_manager.set("user", "name", name)
        self.app.state_manager.set("user", "email", email)

        subject = "Request for GitLab account creation - SkillsHub"
        body = f"Hello,\n\nI would like to request the creation of a GitLab account for the SkillsHub project.\n\nName: {name}\nSchool email: {email}\n\nThank you in advance."
        
        mailto_link = f"mailto:zdenek.velart@vsb.cz?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        
        try:
            webbrowser.open(mailto_link)
            self.app.log_message(f"Email client opened for user: {name}.")
            self.app.state_manager.set("completed_steps", "gitlab_email_sent", True)
        except Exception as e:
            self.app.log_message(f"ERROR opening email: {e}")