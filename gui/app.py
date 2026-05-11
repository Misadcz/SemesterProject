import tkinter as tk
from tkinter import ttk

from core.state_manager import StateManager

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
        
        self.title("SkillsHub Onboarding Tool (VM Edition)")
        self.geometry("800x700")
        self.minsize(700, 600)

        self.state_manager = StateManager()
        
        self.slide_classes = [
            SlideWelcome,          
            SlideVirtualization,   
            SlideVMImport,         
            SlideAccess,           
            SlideWizardConfig,     
            SlideGulpDeploy,        
            SlideEclipse            
        ]
        
        saved_index = self.state_manager.get("progress", "current_slide_index", 0)
        
        if 0 <= saved_index < len(self.slide_classes):
            self.current_slide_index = saved_index
        else:
            self.current_slide_index = 0
            
        self.current_slide_instance = None

        self._build_main_layout()
        
        self.show_slide(self.current_slide_index)

    def _build_main_layout(self):
        
        self.slide_container = tk.Frame(self)
        self.slide_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=25, pady=25)

        self.log_frame = tk.LabelFrame(self, text="System Logs", padx=10, pady=10)
        self.log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

        self.log_text = tk.Text(self.log_frame, height=6, state='disabled', 
                                bg="#f1f3f5", font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END) 
        self.log_text.config(state='disabled')

    def show_slide(self, index):
        if index < 0 or index >= len(self.slide_classes):
            return

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