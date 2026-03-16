import tkinter as tk
from tkinter import ttk
import webbrowser
from gui.slides.base_slide import BaseSlide

# --- Helper class for Hover effect (Tooltip) ---
class ToolTip:
    """Creates a tooltip bubble when hovering over a widget."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True) # Hides classic window borders
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip_window, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("Arial", "9", "normal"), padx=5, pady=3)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

# --- The Slide Itself ---
class SlideDependencies(BaseSlide):
    def build_ui(self):
        tk.Label(self, text="Step 2: Download Java, Liferay, and Freemarker", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        tk.Label(self, text="Download the necessary components. (Left click = Open | Right click = Copy link)").pack(pady=(0, 10))

        # --- JAVA SECTION ---
        java_frame = ttk.LabelFrame(self, text=" 1. Java 1.8 JDK ", padding=(10, 5))
        java_frame.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(java_frame, text="Recommended path: C:/Program Files/Java/").pack(anchor=tk.W, pady=(0, 5))
        java_btn_frame = tk.Frame(java_frame)
        java_btn_frame.pack(fill=tk.X, pady=5)
        
        self.create_link_button(java_btn_frame, "Download from VŠB Cloud (Recommended)", "https://cybercloud.vsb.cz/index.php/f/100226", bg="#d4edda")
        self.create_link_button(java_btn_frame, "Download from Oracle", "https://www.oracle.com/cz/java/technologies/javase/javase8-archive-downloads.html")

        # --- LIFERAY SECTION ---
        liferay_frame = ttk.LabelFrame(self, text=" 2. Liferay Portal 7.3.3-ga4 ", padding=(10, 5))
        liferay_frame.pack(fill=tk.X, padx=20, pady=5)
        liferay_btn_frame = tk.Frame(liferay_frame)
        liferay_btn_frame.pack(fill=tk.X, pady=5)

        self.create_link_button(liferay_btn_frame, "Download from VŠB Cloud (Recommended)", "https://cybercloud.vsb.cz/index.php/f/103557", bg="#d4edda")
        self.create_link_button(liferay_btn_frame, "Download .7z from GitHub", "https://github.com/liferay/liferay-portal/releases/download/7.3.3-ga4/liferay-ce-portal-tomcat-7.3.3-ga4-20200701015330959.7z")
        
        tk.Label(liferay_frame, text="Download the config files and place them into the extracted 'liferay-ce-portal-7.3.3-ga4' folder:").pack(anchor=tk.W, pady=(10,0))
        tk.Label(liferay_frame, text="In this file complete the text: your login and full path to 'liferay-ce-portal-7.3.3-ga4'").pack(anchor=tk.W, pady=(0, 5))
        prop_btn_frame = tk.Frame(liferay_frame)
        prop_btn_frame.pack(fill=tk.X, pady=2)
        
        self.create_link_button(prop_btn_frame, "portal-ext.properties", "https://cybercloud.vsb.cz/index.php/f/103545")
        self.create_link_button(prop_btn_frame, "portal-setup-wizard.properties", "https://cybercloud.vsb.cz/index.php/f/103546")

        # --- FREEMARKER SECTION ---
        freemarker_frame = ttk.LabelFrame(self, text=" 3. Freemarker ", padding=(10, 5))
        freemarker_frame.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(freemarker_frame, text="Download the JAR file and move it to '/liferay-ce-portal-7.3.3-ga4/osgi/modules'").pack(anchor=tk.W, pady=(0, 5))
        fm_btn_frame = tk.Frame(freemarker_frame)
        fm_btn_frame.pack(fill=tk.X, pady=2)

        self.create_link_button(fm_btn_frame, "Download Freemarker JAR", "https://cybercloud.vsb.cz/index.php/f/100944", bg="#d4edda")

        # --- NAVIGATION ---
        nav_frame = tk.Frame(self)
        nav_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Button(nav_frame, text="<- Back", width=15, command=lambda: self.app.prev_slide()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next step ->", width=15, command=lambda: self.app.next_slide()).pack(side=tk.LEFT, padx=5)

    def on_show(self):
        self.app.log_message("Step 2: Displayed links to download Java, Liferay, and Freemarker.")

    # --- HELPER METHODS FOR THIS SLIDE ---

    def create_link_button(self, parent, text, url, bg=None):
        """Creates a button with a link, hover effect, and possibility to copy via right-click."""
        btn = tk.Button(parent, text=text, command=lambda u=url: self.open_link(u))
        if bg:
            btn.config(bg=bg)
        btn.pack(side=tk.LEFT, padx=5)
        
        # Add Tooltip
        ToolTip(btn, f"Link: {url}\n(Right click = copy only)")
        
        # Right-click bind (<Button-3> on Windows/Linux, on Mac it might be <Button-2>)
        btn.bind("<Button-3>", lambda event, u=url: self.copy_only(u))
        return btn

    def copy_only(self, url):
        """Only copies the link to the clipboard (without opening browser)."""
        self.clipboard_clear()
        self.clipboard_append(url)
        self.update()
        self.app.log_message(f"Link copied to clipboard: {url}")

    def open_link(self, url):
        """Opens link in browser and also copies it to clipboard just in case."""
        try:
            self.copy_only(url) # Reusing our method for copying
            webbrowser.open(url)
            self.app.log_message(f"Opening link: {url}")
        except Exception as e:
            self.app.log_message(f"Error opening link: {e}")