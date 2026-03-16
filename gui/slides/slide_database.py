import tkinter as tk
from tkinter import ttk
from gui.slides.base_slide import BaseSlide

class SlideDatabase(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 6: Servers and Local Database", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        # --- SERVERS SECTION ---
        servers_frame = ttk.LabelFrame(self, text=" 1. Servers and Access ", padding=(10, 5))
        servers_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(servers_frame, justify=tk.LEFT, text=(
            "• Staging server: drivescloud.vsb.cz | Production server: drives-compass.eu\n"
            "• To create an account, contact Zdeněk Velart (login = school ID, password will be generated for you).\n"
            "• After logging in to the server, you can change your password using the 'passwd' command."
        )).pack(anchor=tk.W, pady=(0, 5))

        btn_frame1 = tk.Frame(servers_frame)
        btn_frame1.pack(fill=tk.X, pady=2)
        self.create_link_button(btn_frame1, "Download PuTTY (for server access)", "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html")

        # --- DATABASE TOOLS SECTION ---
        tools_frame = ttk.LabelFrame(self, text=" 2. Database Tools ", padding=(10, 5))
        tools_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(tools_frame, justify=tk.LEFT, text=(
            "Install MariaDB with default settings and DBeaver."
        )).pack(anchor=tk.W, pady=(0, 5))

        btn_frame2 = tk.Frame(tools_frame)
        btn_frame2.pack(fill=tk.X, pady=2)
        self.create_link_button(btn_frame2, "Download DBeaver", "https://dbeaver.io/download/")
        self.create_link_button(btn_frame2, "Download MariaDB", "https://mariadb.org/")

        # --- LOCALHOST DB SECTION ---
        local_db_frame = ttk.LabelFrame(self, text=" 3. Localhost DB Setup ", padding=(10, 5))
        local_db_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(local_db_frame, justify=tk.LEFT, text=(
            "1. In DBeaver, create a 'New Database Connection (MariaDB)' (on first launch,\n"
            "   confirm the driver installation).\n"
            "2. In the Main tab, set auth to root / root and test the connection.\n"
            "3. Expand connection, right-click on Databases -> Create New Database:\n"
            "   - Name: liferay | Charset: utf8mb4 | Collation: utf8mb4_general_ci\n"
            "4. To upload data (Restore Database) you will need the dump from staging (see next step)."
        )).pack(anchor=tk.W, pady=(0, 5))

        # --- NAVIGATION ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=10)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 6: Displayed info for Servers and Localhost DB.")