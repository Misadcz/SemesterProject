import tkinter as tk
from tkinter import ttk
from gui.slides.base_slide import BaseSlide

class SlideImport(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 5: Importing Project into Eclipse", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        # --- GRADLE IMPORT SECTION ---
        gradle_frame = ttk.LabelFrame(self, text=" 1. Import Gradle Project ", padding=(10, 5))
        gradle_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(gradle_frame, justify=tk.LEFT, text=(
            "1. In Eclipse, click on: File -> Import -> Existing Gradle Project.\n"
            "2. Select the root folder of the cloned repository (eu.project-drives.platform).\n"
            "3. If an error occurs, go to Preferences -> Gradle and set 'Java home'\n"
            "   to the path of your Java 1.8 installation."
        )).pack(anchor=tk.W, pady=(0, 5))

        # --- LIFERAY SERVER SECTION ---
        server_frame = ttk.LabelFrame(self, text=" 2. Liferay Server Configuration ", padding=(10, 5))
        server_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(server_frame, justify=tk.LEFT, text=(
            "1. In Eclipse, switch to the Liferay perspective (top right).\n"
            "2. In the Servers tab, right-click -> New -> Liferay Server.\n"
            "3. Point 'Liferay Portal Bundle Directory' to the extracted 'liferay-ce-portal-7.3.3-ga4' folder.\n"
            "4. Select JRE: Java SE 8."
        )).pack(anchor=tk.W, pady=(0, 5))
        
        # --- MODULES AND PUBLISHING SECTION ---
        module_frame = ttk.LabelFrame(self, text=" 3. Adding Modules and Publishing ", padding=(10, 5))
        module_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(module_frame, justify=tk.LEFT, text=(
            "1. Double-click to open Liferay Server settings.\n"
            "2. In the 'Publishing' section, select 'Never publish automatically' (prevents freezing).\n"
            "3. Right-click the server -> 'Add and Remove...' -> Add all portal modules to the right."
        )).pack(anchor=tk.W, pady=(0, 5))

        # --- NAVIGATION ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=10)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 5: Displayed instructions for Eclipse import and Liferay server.")