import tkinter as tk
from tkinter import ttk

# Import StateManager pro ukládání postupu
from core.state_manager import StateManager

# Import všech slidů (kroků) průvodce
from gui.slides.slide_eclipse import SlideEclipse
from gui.slides.slide_welcome import SlideWelcome
from gui.slides.slide_virtualization import SlideVirtualization
from gui.slides.slide_vm_import import SlideVMImport
from gui.slides.slide_access import SlideAccess
from gui.slides.slide_wizard_config import SlideWizardConfig
from gui.slides.slide_gulp_deploy import SlideGulpDeploy

class SkillsHubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Základní nastavení okna
        self.title("SkillsHub Onboarding Tool (VM Edition)")
        self.geometry("800x700")
        self.minsize(700, 600)

        # Inicializace správce stavu
        self.state_manager = StateManager()

        # Definice pořadí kroků v aplikaci
        self.slide_classes = [
            SlideWelcome,          # Úvod
            SlideVirtualization,   # Instalace VirtualBoxu
            SlideVMImport,         # Import .ova obrazu
            SlideAccess,           # Žádost o přístup (Zdeněk Velart)
            SlideWizardConfig,     # Konfigurace wizard.properties v VM
            SlideGulpDeploy,        # Spuštění gulp deploy v VM
            SlideEclipse             # Nastavení Eclipse IDE
        ]
        
        # Načtení indexu aktuálního slidu z uloženého JSONu (perzistence)
        saved_index = self.state_manager.get("progress", "current_slide_index", 0)
        
        # Kontrola, zda index odpovídá aktuálnímu počtu slidů
        if 0 <= saved_index < len(self.slide_classes):
            self.current_slide_index = saved_index
        else:
            self.current_slide_index = 0
            
        self.current_slide_instance = None

        # Sestavení GUI layoutu
        self._build_main_layout()
        
        # Zobrazení startovního slidu
        self.show_slide(self.current_slide_index)

    def _build_main_layout(self):
        """Vytvoří hlavní kontejnery pro slidy a logování."""
        
        # Hlavní kontejner pro obsah slidů
        self.slide_container = tk.Frame(self)
        self.slide_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=25, pady=25)

        # Rámeček pro systémové logy v dolní části
        self.log_frame = tk.LabelFrame(self, text="System Logs", padx=10, pady=10)
        self.log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

        # Textové pole pro logy (pouze pro čtení)
        self.log_text = tk.Text(self.log_frame, height=6, state='disabled', 
                                bg="#f1f3f5", font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log_message(self, message):
        """Zapíše zprávu do logovacího okna."""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END) # Automatické odrolování dolů
        self.log_text.config(state='disabled')

    def show_slide(self, index):
        """Přepne aplikaci na zadaný index slidu."""
        if index < 0 or index >= len(self.slide_classes):
            return

        # Uložíme aktuální pozici do JSONu, aby se při restartu pokračovalo tamtéž
        self.state_manager.set("progress", "current_slide_index", index)

        # Pokud už nějaký slide běží, zničíme ho
        if self.current_slide_instance:
            self.current_slide_instance.destroy()

        # Vytvoření instance nového slidu
        SlideClass = self.slide_classes[index]
        self.current_slide_instance = SlideClass(self.slide_container, self)
        self.current_slide_instance.pack(fill=tk.BOTH, expand=True)
        
        self.current_slide_index = index
        
        # Vyvolání události při zobrazení (např. pro logování)
        self.current_slide_instance.on_show()

    def next_slide(self):
        """Posun na další krok."""
        self.show_slide(self.current_slide_index + 1)

    def prev_slide(self):
        """Návrat na předchozí krok."""
        self.show_slide(self.current_slide_index - 1)