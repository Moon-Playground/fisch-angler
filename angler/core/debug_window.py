import customtkinter as ctk


class DebugWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Angler Debug Log")
        self.geometry("400x300")
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.hide)
        
        self.log_textbox = ctk.CTkTextbox(self, font=("Consolas", 12))
        self.log_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_textbox.configure(state="disabled")

    def log(self, formatted_message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", formatted_message)
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def hide(self):
        self.withdraw()
        # Update parent's state if needed
        if hasattr(self.master, "debug_var"):
            self.master.debug_var.set(False)

    def show(self):
        self.deiconify()
        self.lift()