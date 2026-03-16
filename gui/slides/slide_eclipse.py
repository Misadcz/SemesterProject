import tkinter as tk
from tkinter import ttk
import os
import sys
import subprocess
import threading
from pathlib import Path
from gui.slides.base_slide import BaseSlide

class SlideEclipse(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Krok 4: Instalace a konfigurace Eclipse", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        # --- SEKCE ECLIPSE IDE ---
        eclipse_frame = ttk.LabelFrame(self, text=" 1. Eclipse IDE (2020-06) ", padding=(10, 5))
        eclipse_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(eclipse_frame, justify=tk.LEFT, text=(
            "Spusťte přiložený instalátor Eclipse a postupujte takto:\n"
            "1. Vyberte 'Eclipse IDE for Enterprise Java Developers'.\n"
            "2. Nainstalujte a zavřete instalátor.\n"
            "DŮLEŽITÉ: Po instalaci najděte eclipse.ini a nastavte v něm cestu k Javě (min. 17!)."
        )).pack(anchor=tk.W, pady=(0, 5))

        btn_frame = tk.Frame(eclipse_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Tlačítko pro spuštění offline instalace
        self.install_btn = tk.Button(btn_frame, text="⚙️ Spustit instalaci Eclipse", 
                                     font=("Arial", 10, "bold"), bg="#d4edda", 
                                     command=self.start_installation)
        self.install_btn.pack(side=tk.LEFT, padx=5)

        # --- SEKCE LIFERAY PLUGIN (VIDEO) ---
        plugin_frame = ttk.LabelFrame(self, text=" 2. Liferay Eclipse plugin ", padding=(10, 5))
        plugin_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(plugin_frame, text="Návod: Instalace Liferay pluginu přes Eclipse Marketplace").pack(anchor=tk.W, pady=(0, 5))

        # Tlačítko pro přehrání videa
        play_btn = tk.Button(plugin_frame, text="▶ Otevřít video návod", font=("Arial", 10, "bold"), bg="#cce5ff", command=self.play_video)
        play_btn.pack(anchor=tk.W, pady=10, padx=5)

        # --- NAVIGACE ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=10)
        
        tk.Button(nav_frame, text="<- Zpět", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Další krok ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Krok 4: Zobrazeny pokyny pro instalaci Eclipse z lokálních souborů.")

    # --- METODY PRO INSTALACI ---
    def start_installation(self):
        """Spustí instalační proces v novém vlákně."""
        # Vizuální změna tlačítka, aby uživatel věděl, že má čekat
        self.install_btn.config(text="⏳ Instalátor běží...", state=tk.DISABLED, bg="#f8d7da")
        self.app.log_message("Spouštím instalátor Eclipse. Prosím, projděte instalačním procesem v novém okně.")

        # Spuštění ve vlákně
        install_thread = threading.Thread(target=self._run_installer_in_background)
        install_thread.daemon = True 
        install_thread.start()

    def _run_installer_in_background(self):
        """Běží na pozadí a čeká na dokončení instalace."""
        base_dir = Path(__file__).resolve().parent.parent.parent
        # Cesta odpovídá tvé stromové struktuře
        installer_path = base_dir / "libs" / "eclipse-inst-win64 (202-06 R).exe"

        if not installer_path.exists():
            # GUI prvky smíme upravovat jen přes master.after z hlavního vlákna
            self.app.after(0, self._on_install_error, f"Soubor nenalezen: {installer_path.name}")
            return

        try:
            # subprocess.run čeká na zavření spuštěného programu
            subprocess.run([str(installer_path)], check=True)
            self.app.after(0, self._on_install_success)
        except Exception as e:
            self.app.after(0, self._on_install_error, str(e))

    def _on_install_success(self):
        """Volá se z hlavního vlákna po zavření instalátoru."""
        self.install_btn.config(text="✔ Instalační proces dokončen", bg="#d4edda", state=tk.NORMAL)
        self.app.log_message("Instalátor Eclipse byl ukončen.")

    def _on_install_error(self, error_msg):
        """Volá se z hlavního vlákna v případě chyby."""
        self.install_btn.config(text="❌ Chyba (Zkusit znovu)", bg="#f5c6cb", state=tk.NORMAL)
        self.app.log_message(f"CHYBA při spouštění instalátoru: {error_msg}")

    # --- METODA PRO VIDEO ---
    def play_video(self):
        """Otevře video návod ve výchozím systémovém přehrávači."""
        base_dir = Path(__file__).resolve().parent.parent.parent
        video_path = base_dir / "assets" / "liferay_in_eclipse_1.mp4"

        if not video_path.exists():
            self.app.log_message(f"CHYBA: Video nebylo nalezeno na cestě: {video_path}")
            return

        try:
            self.app.log_message(f"Spouštím video: {video_path.name}")
            if sys.platform == "win32":
                os.startfile(video_path)
            elif sys.platform == "darwin":  
                subprocess.call(["open", str(video_path)])
            else:  
                subprocess.call(["xdg-open", str(video_path)])
        except Exception as e:
            self.app.log_message(f"Chyba při přehrávání videa: {e}")