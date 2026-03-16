import tkinter as tk
from tkinter import ttk
from gui.slides.base_slide import BaseSlide

class SlideStaging(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 7: Staging DB and Data Dump", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        # --- STAGING CONNECTION SECTION ---
        staging_frame = ttk.LabelFrame(self, text=" 1. Connecting to Staging DB (DBeaver) ", padding=(10, 5))
        staging_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(staging_frame, justify=tk.LEFT, text=(
            "To get the database, you must connect to the Staging server (drivescloud.vsb.cz).\n"
            "In DBeaver, create a 'New Database Connection (MariaDB)':\n\n"
            "• Main tab: Leave default settings. Auth: your staging username and password.\n"
            "• Click '+' next to 'SSH, SSL, Proxy' and select SSH.\n"
            "• SSH tab: Host/IP: drivescloud.vsb.cz | Port: 22 | Password: your staging password.\n"
            "• Click 'Test Connection...' to verify."
        )).pack(anchor=tk.W, pady=(0, 5))

        # --- DATABASE DUMP SECTION ---
        dump_frame = ttk.LabelFrame(self, text=" 2. Creating a Database Dump ", padding=(10, 5))
        dump_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(dump_frame, justify=tk.LEFT, text=(
            "Once connected to Staging, you can download the current data:\n\n"
            "1. Expand staging connection -> Databases.\n"
            "2. Right-click on the 'liferay' database -> Tools -> Dump Database.\n"
            "3. Leave default settings -> Next.\n"
            "4. Set the output folder and click Start.\n\n"
            "Import the generated .sql file into your local database (previous step)."
        )).pack(anchor=tk.W, pady=(0, 5))

        # --- NAVIGATION ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=10)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Finish", width=15, command=self.finish_setup, bg="#d4edda").pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 7: Displayed instructions for SSH connection and creating DB dump.")

    def finish_setup(self):
        self.app.log_message("--- ONBOARDING FINISHED ---")
        self.app.log_message("All instructions have been provided. The local development environment should be ready.")