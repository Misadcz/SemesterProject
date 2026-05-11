import tkinter as tk
import webbrowser


class ToolTip:
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
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("Arial", "9", "normal"), padx=5, pady=3)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class BaseSlide(tk.Frame):
    def __init__(self, parent_container, app_controller):
        super().__init__(parent_container)
        self.app = app_controller
        self.columnconfigure(0, weight=1)
        self.build_ui()

    def build_ui(self):
        pass

    def on_show(self):
        pass

    def create_link_button(self, parent, text, url, bg=None):
        btn = tk.Button(parent, text=text, command=lambda u=url: self.open_link(u))
        if bg:
            btn.config(bg=bg)
        btn.pack(side=tk.LEFT, padx=5)
        ToolTip(btn, f"Link: {url}\n(Right click = copy only)")
        btn.bind("<Button-3>", lambda event, u=url: self.copy_only(u))
        return btn

    def copy_only(self, url):
        self.clipboard_clear()
        self.clipboard_append(url)
        self.update()
        self.app.log_message(f"Link copied to clipboard: {url}")

    def open_link(self, url):
        try:
            self.copy_only(url)
            webbrowser.open(url)
            self.app.log_message(f"Opening link: {url}")
        except Exception as e:
            self.app.log_message(f"Error opening link: {e}")