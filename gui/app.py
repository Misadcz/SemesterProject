import tkinter as tk
from tkinter import ttk

# Import StateManager
from core.state_manager import StateManager

# Import our slides
from gui.slides.slide_welcome import SlideWelcome
from gui.slides.slide_gitlab import SlideGitLab
from gui.slides.slide_dependencies import SlideDependencies
from gui.slides.slide_themes import SlideThemes
from gui.slides.slide_eclipse import SlideEclipse
from gui.slides.slide_import import SlideImport
from gui.slides.slide_database import SlideDatabase
from gui.slides.slide_staging import SlideStaging

class SkillsHubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SkillsHub Onboarding Tool")
        self.geometry("750x650")
        self.minsize(650, 500)

        # Initialize StateManager
        self.state_manager = StateManager()

        # List of slide classes in order
        self.slide_classes = [
            SlideWelcome,
            SlideGitLab,
            SlideDependencies,
            SlideThemes,
            SlideEclipse,
            SlideImport,
            SlideDatabase,
            SlideStaging
        ]
        
        # --- ZMĚNA ZDE: Načtení indexu z uloženého stavu ---
        # Pokud uživatel aplikaci ještě nikdy nezapnul, vrátí to výchozí hodnotu 0 (Welcome Slide)
        saved_index = self.state_manager.get("progress", "current_slide_index", 0)
        
        # Pro jistotu zkontrolujeme, zda se index nevymyká počtu slidů (kdybychom v kódu nějaký slide smazali)
        if 0 <= saved_index < len(self.slide_classes):
            self.current_slide_index = saved_index
        else:
            self.current_slide_index = 0
            
        self.current_slide_instance = None

        self._build_main_layout()
        self.show_slide(self.current_slide_index)

    def _build_main_layout(self):
        self.slide_container = tk.Frame(self)
        self.slide_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.log_frame = tk.LabelFrame(self, text="System Logs", padx=5, pady=5)
        self.log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.log_text = tk.Text(self.log_frame, height=6, state='disabled', bg="#f8f9fa")
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def show_slide(self, index):
        if index < 0 or index >= len(self.slide_classes):
            return

        # --- ZMĚNA ZDE: Uložení aktuální pozice do JSONu při každém přesunu ---
        self.state_manager.set("progress", "current_slide_index", index)

        if self.current_slide_instance:
            self.current_slide_instance.destroy()

        SlideClass = self.slide_classes[index]
        self.current_slide_instance = SlideClass(self.slide_container, self)
        self.current_slide_instance.pack(fill=tk.BOTH, expand=True)
        
        self.current_slide_index = index
        self.current_slide_instance.on_show()

    def next_slide(self):
        self.show_slide(self.current_slide_index + 1)

    def prev_slide(self):
        self.show_slide(self.current_slide_index - 1)