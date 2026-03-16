import tkinter as tk
from tkinter import ttk
import threading
import zipfile
import tarfile
import shutil
from pathlib import Path
from gui.slides.base_slide import BaseSlide

class SlideDependencies(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 2: Setup Java and Liferay", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        tk.Label(self, text="Components will be extracted from the 'libs' folder into your Workspace.").pack(pady=(0, 10))

        # --- JAVA SECTION ---
        java_frame = ttk.LabelFrame(self, text=" 1. Java 1.8 JDK ", padding=(10, 5))
        java_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(java_frame, justify=tk.LEFT, text=(
            "Click below to extract the offline Java package to the local Workspace."
        )).pack(anchor=tk.W, pady=(0, 5))
        
        self.java_btn = tk.Button(java_frame, text="📦 Extract Java (JDK 1.8)", bg="#cce5ff", font=("Arial", 10, "bold"),
                                  command=self.extract_java)
        self.java_btn.pack(anchor=tk.W, pady=5, padx=5)

        # --- LIFERAY & CONFIG SECTION ---
        liferay_frame = ttk.LabelFrame(self, text=" 2. Liferay Portal & Configurations ", padding=(10, 5))
        liferay_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(liferay_frame, justify=tk.LEFT, text=(
            "This will extract the Liferay Portal (.tar.gz), copy the configuration files\n"
            "(portal-ext, portal-setup-wizard), and install the Freemarker module automatically."
        )).pack(anchor=tk.W, pady=(0, 5))

        self.liferay_btn = tk.Button(liferay_frame, text="📦 Extract Liferay & Apply Configs", bg="#cce5ff", font=("Arial", 10, "bold"),
                                     command=self.extract_liferay)
        self.liferay_btn.pack(anchor=tk.W, pady=5, padx=5)

        # --- NAVIGATION ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 2: Ready to extract offline dependencies.")
        
        # Check if Java is already extracted
        saved_java_path = self.app.state_manager.get("paths", "java_home")
        if saved_java_path and Path(saved_java_path).exists():
            self.java_btn.config(text="✔ Java is already extracted", state=tk.DISABLED, bg="#d4edda")

        # Check if Liferay is already extracted
        saved_liferay_path = self.app.state_manager.get("paths", "liferay_home")
        if saved_liferay_path and Path(saved_liferay_path).exists():
            self.liferay_btn.config(text="✔ Liferay is already extracted", state=tk.DISABLED, bg="#d4edda")

    # --- JAVA EXTRACTION ---
    def extract_java(self):
        self.java_btn.config(text="⏳ Extracting Java (Please wait)...", state=tk.DISABLED, bg="#f8d7da")
        self.app.log_message("Starting background extraction of JDK...")

        extract_thread = threading.Thread(target=self._run_java_extraction)
        extract_thread.daemon = True
        extract_thread.start()

    def _run_java_extraction(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        zip_path = base_dir / "libs" / "jdk1.8.0_202.zip"
        workspace_dir = base_dir / "Workspace"

        if not zip_path.exists():
            self.app.after(0, self._on_java_error, f"File {zip_path.name} not found in 'libs'!")
            return

        try:
            workspace_dir.mkdir(exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(workspace_dir)

            extracted_java_path = workspace_dir / "jdk1.8.0_202"
            self.app.state_manager.set("paths", "java_home", str(extracted_java_path))

            self.app.after(0, self._on_java_success)
        except Exception as e:
            self.app.after(0, self._on_java_error, str(e))

    def _on_java_success(self):
        self.java_btn.config(text="✔ Java successfully extracted", bg="#d4edda")
        self.app.log_message("JDK was extracted successfully. Path saved.")

    def _on_java_error(self, error_msg):
        self.java_btn.config(text="❌ Extraction error (Try again)", state=tk.NORMAL, bg="#f5c6cb")
        self.app.log_message(f"ERROR: {error_msg}")

    # --- LIFERAY EXTRACTION ---
    def extract_liferay(self):
        self.liferay_btn.config(text="⏳ Extracting Liferay (This may take a few minutes)...", state=tk.DISABLED, bg="#f8d7da")
        self.app.log_message("Starting background extraction of Liferay Portal...")

        extract_thread = threading.Thread(target=self._run_liferay_extraction)
        extract_thread.daemon = True
        extract_thread.start()

    def _run_liferay_extraction(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        libs_dir = base_dir / "libs"
        workspace_dir = base_dir / "Workspace"
        
        tar_path = libs_dir / "liferay-ce-portal-tomcat-7.3.3-ga4-20200701015330959.tar.gz"

        if not tar_path.exists():
            self.app.after(0, self._on_liferay_error, f"File {tar_path.name} not found in 'libs'!")
            return

        try:
            workspace_dir.mkdir(exist_ok=True)
            
            # 1. Extract Liferay (.tar.gz)
            with tarfile.open(tar_path, 'r:gz') as tar_ref:
                tar_ref.extractall(workspace_dir)

            liferay_dir = workspace_dir / "liferay-ce-portal-7.3.3-ga4"
            
            # 2. Copy properties files
            prop_ext = libs_dir / "portal-ext.properties"
            prop_wizard = libs_dir / "portal-setup-wizard.properties"
            
            if prop_ext.exists():
                shutil.copy(prop_ext, liferay_dir / "portal-ext.properties")
            if prop_wizard.exists():
                shutil.copy(prop_wizard, liferay_dir / "portal-setup-wizard.properties")

            # 3. Copy Freemarker module
            freemarker_jar = libs_dir / "org.freemarker_2.3.22.v20160210-1233.jar"
            osgi_modules_dir = liferay_dir / "osgi" / "modules"
            
            if freemarker_jar.exists():
                osgi_modules_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy(freemarker_jar, osgi_modules_dir / "org.freemarker_2.3.22.v20160210-1233.jar")

            # Save path to state
            self.app.state_manager.set("paths", "liferay_home", str(liferay_dir))

            self.app.after(0, self._on_liferay_success)
        except Exception as e:
            self.app.after(0, self._on_liferay_error, str(e))

    def _on_liferay_success(self):
        self.liferay_btn.config(text="✔ Liferay and configs applied", bg="#d4edda")
        self.app.log_message("Liferay Portal, configurations, and Freemarker were successfully set up.")

    def _on_liferay_error(self, error_msg):
        self.liferay_btn.config(text="❌ Extraction error (Try again)", state=tk.NORMAL, bg="#f5c6cb")
        self.app.log_message(f"ERROR: {error_msg}")