import tkinter as tk


class CaptureBox(tk.Toplevel):
    def __init__(
        self,
        box_color: str = "blue",
        box_alpha: float = 0.3,
        box_x: int = 122,
        box_y: int = 40,
        box_width: int = 100,
        box_height: int = 50,
        text: str = ""
    ):
        super().__init__()
        self.capture_width, self.capture_height = box_width, box_height
        self.capture_x, self.capture_y = box_x, box_y
        self.geometry(f"{self.capture_width}x{self.capture_height}+{self.capture_x}+{self.capture_y}")
        self.overrideredirect(True)
        self.configure(bg=box_color, highlightthickness=2, highlightbackground="white")

        self.attributes("-alpha", box_alpha)
        self.attributes("-topmost", True)

        self.border_width = 8
        self.min_size = 20

        self.text_label = tk.Label(self, text=text, bg=box_color, fg="white", font=("Arial", 12))
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")

        # Bindings
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Motion>", self.update_cursor)

        self.mode = None # "move" or resize directions like "n", "s", "e", "w", "nw", etc.

    def update_cursor(self, event):
        edge = self.get_edge(event.x, event.y)
        if edge == "n" or edge == "s":
            self.config(cursor="sb_v_double_arrow")
        elif edge == "e" or edge == "w":
            self.config(cursor="sb_h_double_arrow")
        elif edge == "nw" or edge == "se":
            self.config(cursor="top_left_corner")
        elif edge == "ne" or edge == "sw":
            self.config(cursor="top_right_corner")
        else:
            self.config(cursor="fleur")

    def get_edge(self, x, y):
        edge = ""
        if y < self.border_width: edge += "n"
        elif y > self.winfo_height() - self.border_width: edge += "s"
        if x < self.border_width: edge += "w"
        elif x > self.winfo_width() - self.border_width: edge += "e"
        return edge

    def on_press(self, event):
        self.mode = self.get_edge(event.x, event.y) or "move"
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.orig_x = self.winfo_x()
        self.orig_y = self.winfo_y()
        self.orig_width = self.winfo_width()
        self.orig_height = self.winfo_height()

    def on_drag(self, event):
        dx = event.x_root - self.start_x
        dy = event.y_root - self.start_y

        new_x, new_y = self.orig_x, self.orig_y
        new_w, new_h = self.orig_width, self.orig_height

        if self.mode == "move":
            new_x = self.orig_x + dx
            new_y = self.orig_y + dy
        else:
            if "n" in self.mode:
                h = max(self.min_size, self.orig_height - dy)
                new_y = self.orig_y + (self.orig_height - h)
                new_h = h
            elif "s" in self.mode:
                new_h = max(self.min_size, self.orig_height + dy)

            if "w" in self.mode:
                w = max(self.min_size, self.orig_width - dx)
                new_x = self.orig_x + (self.orig_width - w)
                new_w = w
            elif "e" in self.mode:
                new_w = max(self.min_size, self.orig_width + dx)

        self.capture_x, self.capture_y = new_x, new_y
        self.capture_width, self.capture_height = new_w, new_h
        self.geometry(f"{new_w}x{new_h}+{new_x}+{new_y}")

