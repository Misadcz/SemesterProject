import tkinter as tk
from tkinter import ttk
from gui.slides.base_slide import BaseSlide

class SlideEclipse(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 4: Eclipse IDE Setup", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        # --- SEKCE 1: Kde najít Eclipse ---
        loc_frame = ttk.LabelFrame(self, text=" 1. Launch Eclipse ", padding=(10, 5))
        loc_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(loc_frame, justify=tk.LEFT, text=(
            "Eclipse IDE is already downloaded and prepared for you.\n"
            "• Open your file manager or terminal.\n"
            "• Navigate to the folder:  ~/Documents/eclipse/\n"
            "• Run the 'eclipse' executable to start the IDE."
        )).pack(anchor=tk.W, pady=5)

        # --- SEKCE 2: Jak importovat projekt ---
        import_frame = ttk.LabelFrame(self, text=" 2. Import the Project ", padding=(10, 5))
        import_frame.pack(fill=tk.X, padx=20, pady=10)

        instructions = (
            "Once Eclipse is running, you need to import the repository you just cloned:\n\n"
            "1. In the top menu, go to: File -> Import...\n"
            "2. Select: Gradle -> Existing Gradle Project and click Next.\n"
            "3. In the 'Project root directory' field, browse to your cloned folder:\n"
            "   (e.g., .../platform/eu.project-drives.platform)\n"
            "4. Click Finish and let Gradle sync the project."
        )
        tk.Label(import_frame, justify=tk.LEFT, text=instructions).pack(anchor=tk.W, pady=5)

        # --- NAVIGATION ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)