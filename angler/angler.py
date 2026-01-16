import asyncio
import dxcam_cpp as dxcam

import tkinter as tk
import customtkinter as ctk
import threading
import os
import pydirectinput
import time

from angler.core.capture_box import CaptureBox
from angler.core.debug_window import DebugWindow
from angler.utils import Utils

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AnglerApp(ctk.CTk, Utils):
    def __init__(self):
        super().__init__()
        self.active = threading.Event()
        self.force_stop = threading.Event()
        self.title("Angler")
        self.geometry("510x350")
        
        # Load config first
        self.config_data = self.load_config()
        
        self.camera = dxcam.create()
        self.capture_box = CaptureBox(
            box_color="blue",
            box_alpha=0.3,
            text=""
        )
        self.capture_box.capture_width = self.config_data['ocr']['capture_width']
        self.capture_box.capture_height = self.config_data['ocr']['capture_height']
        self.capture_box.capture_x = self.config_data['ocr']['capture_x']
        self.capture_box.capture_y = self.config_data['ocr']['capture_y']
        self.enable_overlay = self.config_data['ui']['enable_overlay']
        self.enable_debug = self.config_data['ui'].get('enable_debug', True)
        
        self.ocr_backend = self.config_data['ocr']['backend'] if self.test_tesseract() else "winrt"
        self.ocr_engine_tesseract = self.init_ocr_engine_tesseract()
        self.ocr_engine_winrt = self.init_ocr_engine_winrt()
        self.ocr_engine = self.ocr_engine_tesseract if self.ocr_backend == "tesseract" else self.ocr_engine_winrt
        self.fish_area_x = self.config_data.get('coordinates', {}).get('fish_area_x', 0)
        self.fish_area_y = self.config_data.get('coordinates', {}).get('fish_area_y', 0)
        self.dialogue_x = self.config_data.get('coordinates', {}).get('dialogue_x', 0)
        self.dialogue_y = self.config_data.get('coordinates', {}).get('dialogue_y', 0)
        self.search_bar_x = self.config_data.get('coordinates', {}).get('search_bar_x', 0)
        self.search_bar_y = self.config_data.get('coordinates', {}).get('search_bar_y', 0)
        self.loop_delay = self.config_data["delay"]["loop"]
        self.initial_delay = self.config_data["delay"]["initial"]
        self.typing_delay = self.config_data["delay"]["typing"]
        self.inv_delay = self.config_data["delay"]["inv"]
        self.action_delay = self.config_data["delay"]["action"]
        self.angler_location = self.config_data["misc"]["angler_location"]
        self.last_fish = None

        # StringVars for UI bindings
        self.loop_delay_var = ctk.StringVar(value=str(self.loop_delay))
        self.initial_delay_var = ctk.StringVar(value=str(self.initial_delay))
        self.typing_delay_var = ctk.StringVar(value=str(self.typing_delay))
        self.inv_delay_var = ctk.StringVar(value=str(self.inv_delay))
        self.action_delay_var = ctk.StringVar(value=str(self.action_delay))

        # Coordinate StringVars
        self.fish_area_var = ctk.StringVar(value=f"x: {self.fish_area_x}, y: {self.fish_area_y}")
        self.search_bar_var = ctk.StringVar(value=f"x: {self.search_bar_x}, y: {self.search_bar_y}")
        self.dialogue_var = ctk.StringVar(value=f"x: {self.dialogue_x}, y: {self.dialogue_y}")

        # Debug Window
        self.debug_window = DebugWindow(self)
        if not self.enable_debug:
            self.debug_window.withdraw()

        # Bind virtual events
        self.bind("<<ToggleBox>>", lambda e: self._toggle_box())
        self.bind("<<ToggleAction>>", lambda e: self._toggle_action())
        self.bind("<<ExitApp>>", lambda e: self._exit_app())
        self.bind("<<TestCapture>>", lambda e: self._test_capture())

        self.setup_ui()
        self.apply_hotkeys()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Status Window (Standard TK for simpler overlay management)
        self.status_window = None
        self.create_status_window()
        if not self.enable_overlay:
            self.hide_status_window()
        self.after(200, lambda: self._set_icon())

    def _set_icon(self):
        self.find_and_set_icon()

    def _test_capture(self):
        frame = self.capture_screen()
        if frame is not None:
            try:
                # Run async OCR in a synchronous context
                text = asyncio.run(self.read_frame(frame))
                #print(f"OCR Result: '{text}'")
                self.show_capture_dialog(frame, text)
            except Exception as e:
                #print(f"OCR Error: {e}")
                self.show_capture_dialog(frame=None, text=f"Failed to read frame: {e}")
        else:
            print("Capture returned None (check if box is within screen bounds)")
        print("-----------------------")

    def setup_ui(self):
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.home_tab = self.tab_view.add("Home")
        self.coordinates_tab = self.tab_view.add("Coordinates")
        self.delays_tab = self.tab_view.add("Delays")
        self.general_tab = self.tab_view.add("General")
        self.hotkeys_tab = self.tab_view.add("Hotkeys")

        # --- HOME TAB ---
        self.description = ctk.CTkLabel(
            self.home_tab, 
            text="""
Angler Quest macro for roblox fisch.
Make sure to turn off favorites in the inventory ui before using this macro.
Don't enable debug log if you plan to use the macro for long periods of time.
            """, 
            font=("Arial", 14)
        )
        self.description.pack(pady=10)

        self.status_label = ctk.CTkLabel(self.home_tab, text="Status: Inactive", text_color="red", font=("Arial", 16, "bold"))
        self.status_label.pack(pady=10)

        self.info_label = ctk.CTkLabel(self.home_tab, text="Settings and Hotkeys are now in separate tabs", font=("Arial", 12))
        self.info_label.pack(pady=10)

        # --- COORDINATES TAB ---
        self.coordinates_frame = ctk.CTkFrame(self.coordinates_tab)
        self.coordinates_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.coordinates_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.coordinates_frame, text="Click Locations", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(10, 5))

        ctk.CTkLabel(self.coordinates_frame, text="Fish area").grid(row=1, column=0, padx=15, pady=15, sticky="w")
        ctk.CTkLabel(self.coordinates_frame, textvariable=self.fish_area_var).grid(row=1, column=1, padx=10, pady=15, sticky="ew")
        ctk.CTkButton(self.coordinates_frame, text="Select", command=self.select_fish_area).grid(row=1, column=2, padx=10, pady=15, sticky="ew")

        ctk.CTkLabel(self.coordinates_frame, text="Search bar").grid(row=2, column=0, padx=15, pady=15, sticky="w")
        ctk.CTkLabel(self.coordinates_frame, textvariable=self.search_bar_var).grid(row=2, column=1, padx=10, pady=15, sticky="ew")
        ctk.CTkButton(self.coordinates_frame, text="Select", command=self.select_search_bar).grid(row=2, column=2, padx=10, pady=15, sticky="ew")

        ctk.CTkLabel(self.coordinates_frame, text="Dialogue").grid(row=3, column=0, padx=15, pady=15, sticky="w")
        ctk.CTkLabel(self.coordinates_frame, textvariable=self.dialogue_var).grid(row=3, column=1, padx=10, pady=15, sticky="ew")
        ctk.CTkButton(self.coordinates_frame, text="Select", command=self.select_dialogue).grid(row=3, column=2, padx=10, pady=15, sticky="ew")

        # --- GENERAL TAB ---
        self.general_frame = ctk.CTkFrame(self.general_tab)
        self.general_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.general_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.general_frame, text="General Settings", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # angler location
        ctk.CTkLabel(self.general_frame, text="Angler Location").grid(row=1, column=0, padx=15, pady=15, sticky="w")
        self.angler_location_var = ctk.StringVar(value=self.angler_location)
        angler_location_list = list(self.config_data["fish_list"].keys())
        ctk.CTkOptionMenu(self.general_frame, variable=self.angler_location_var, values=angler_location_list).grid(row=1, column=1, padx=10, pady=15, sticky="ew")
        self.angler_location_var.trace_add("write", lambda *args: self._update_angler_location())

        ctk.CTkLabel(self.general_frame, text="OCR Backend").grid(row=2, column=0, padx=15, pady=15, sticky="w")
        self.backend_var = ctk.StringVar(value=self.ocr_backend)
        backend_list = ["winrt"]
        if self.test_tesseract():
            backend_list.append("tesseract")
        backend_cb = ctk.CTkOptionMenu(self.general_frame, variable=self.backend_var, values=backend_list)
        backend_cb.grid(row=2, column=1, padx=10, pady=15, sticky="ew")
        self.backend_var.trace_add("write", lambda *args: self._update_ocr_backend())

        # Overlay entries
        ctk.CTkLabel(self.general_frame, text="Status Overlay").grid(row=3, column=0, padx=15, pady=15, sticky="w")
        self.overlay_var = ctk.BooleanVar(value=self.enable_overlay)
        overlay_cb = ctk.CTkSwitch(self.general_frame, text="", variable=self.overlay_var, command=self._update_overlay)
        overlay_cb.grid(row=3, column=1, padx=10, pady=15, sticky="ew")

        ctk.CTkLabel(self.general_frame, text="Debug Log").grid(row=4, column=0, padx=15, pady=15, sticky="w")
        self.debug_var = ctk.BooleanVar(value=self.enable_debug)
        debug_cb = ctk.CTkSwitch(self.general_frame, text="", variable=self.debug_var, command=self._update_debug)
        debug_cb.grid(row=4, column=1, padx=10, pady=15, sticky="ew")

        # --- DELAYS TAB ---
        self.delay_frame = ctk.CTkFrame(self.delays_tab)
        self.delay_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.delay_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.delay_frame, text="Timing Delays (seconds)", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=(10, 5))

        def add_delay_row(row, label, var, cmd, col=1, colspan=1):
            ctk.CTkLabel(self.delay_frame, text=label).grid(row=row, column=0 if col==1 else 2, padx=15, pady=15, sticky="w")
            entry = ctk.CTkEntry(self.delay_frame, textvariable=var)
            entry.grid(row=row, column=1 if col==1 else 3, columnspan=colspan, padx=10, pady=15, sticky="ew")
            var.trace_add("write", lambda *args: cmd())

        add_delay_row(1, "Initial Delay", self.initial_delay_var, self._update_initial_delay, 1)
        add_delay_row(1, "Action Delay", self.action_delay_var, self._update_action_delay, 2)
        add_delay_row(2, "Inv Delay", self.inv_delay_var, self._update_inv_delay, 1)
        add_delay_row(2, "Typing Delay", self.typing_delay_var, self._update_typing_delay, 2)
        add_delay_row(3, "Loop Delay", self.loop_delay_var, self._update_loop_delay, 1, 3)

        # --- HOTKEYS TAB ---
        self.hotkeys_frame = ctk.CTkFrame(self.hotkeys_tab)
        self.hotkeys_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.hotkeys_frame.grid_columnconfigure(1, weight=1)

        # Hotkey Entries
        self.hk_entries = {}

        def add_hk_row(row, label, key):
            ctk.CTkLabel(self.hotkeys_frame, text=label).grid(row=row, column=0, padx=15, pady=15, sticky="w")
            entry = ctk.CTkEntry(self.hotkeys_frame)
            current_val = self.config_data['hotkeys'].get(key, "")
            entry.insert(0, current_val)
            entry.grid(row=row, column=1, padx=10, pady=15, sticky="ew")
            self.hk_entries[key] = entry

        add_hk_row(0, "Test Capture:", "test_capture")
        add_hk_row(1, "Toggle Box:", "toggle_box")
        add_hk_row(2, "Start/Stop:", "toggle_action")
        add_hk_row(3, "Exit App:", "exit_app")

        self.save_btn = ctk.CTkButton(self.hotkeys_frame, text="Save & Apply", command=self.save_and_apply_config)
        self.save_btn.grid(row=4, column=0, columnspan=2, pady=20)

    def log(self, message):
        """Thread-safe logging to the DebugWindow."""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        def _update():
            if self.debug_window:
                self.debug_window.log(formatted_message)
        
        self.after(0, _update)

    def create_status_window(self):
        if self.status_window:
            try:
                self.status_window.destroy()
            except:
                pass
        self.status_window = tk.Toplevel(self)
        self.status_window.title("Angler Macro Status")
        
        # Load pos from config or default
        sx = self.config_data.get('ui', {}).get('status_x', 100)
        sy = self.config_data.get('ui', {}).get('status_y', 100)
        self.status_window.geometry(f"150x20+{sx}+{sy}")

        self.status_window.attributes("-topmost", True)
        self.status_window.attributes("-alpha", 0.7) # Semi-transparent
        self.status_window.overrideredirect(True)    # Borderless
        
        # Style
        self.status_window.configure(bg="black")
        self.status_lbl_widget = tk.Label(self.status_window, text="Angler Macro: Inactive", font=("Arial", 10, "bold"), bg="black", fg="white")
        self.status_lbl_widget.pack(expand=True, fill="both")
        
        # Drag functionality
        self.status_window.bind("<ButtonPress-1>", self.start_status_move)
        self.status_window.bind("<B1-Motion>", self.do_status_move)
        self.status_window.bind("<ButtonRelease-1>", self.stop_status_move)
        
        self.status_lbl_widget.bind("<ButtonPress-1>", self.start_status_move)
        self.status_lbl_widget.bind("<B1-Motion>", self.do_status_move)
        self.status_lbl_widget.bind("<ButtonRelease-1>", self.stop_status_move)

        #self.hide_status_window()

    def start_status_move(self, event):
        self.status_drag_x = event.x
        self.status_drag_y = event.y

    def do_status_move(self, event):
        x = self.status_window.winfo_x() - self.status_drag_x + event.x
        y = self.status_window.winfo_y() - self.status_drag_y + event.y
        self.status_window.geometry(f"+{x}+{y}")
        
        # Update config directly (debounce could be better but this is fine for now)
        if "ui" not in self.config_data:
            self.config_data["ui"] = {}
        self.config_data["ui"]["status_x"] = x
        self.config_data["ui"]["status_y"] = y
        # We can save on mouse release ideally, but implicit save on exit is safer for perf
        # Let's bind ButtonRelease to save
        
    def stop_status_move(self, event):
        if "ui" not in self.config_data:
            self.config_data["ui"] = {}
        self.config_data["ui"]["status_x"] = self.status_window.winfo_x()
        self.config_data["ui"]["status_y"] = self.status_window.winfo_y()
        self.save_config_file(self.config_data)

    def hide_status_window(self):
        self.status_window.withdraw()

    def show_status_window(self):
        self.status_window.deiconify()
        self.status_window.lift()

    def _toggle_action(self):
        if self.active.is_set():
            self.active.clear()
            self.status_lbl_widget.config(text="Angler: Inactive")
            self.status_label.configure(text="Angler: Inactive", text_color="red")
        else:
            self.active.set()
            self.status_lbl_widget.config(text="Angler: Active")
            self.status_label.configure(text="Angler: Active", text_color="green")
            self.show_status_window()

    def _toggle_box(self):
        if self.capture_box.state() == "withdrawn":
            self.capture_box.deiconify()
        else:
            self.save_config_coords()
            self.capture_box.withdraw()

    def _exit_app(self):
        self.force_stop.set()
        self.quit()

    def on_close(self):
        self.force_stop.set()
        self.destroy()
        os._exit(0)

    def capture_screen(self):
        return self.capture_screen_region()

    def _update_angler_location(self):
        self.angler_location = self.angler_location_var.get()
        if "misc" not in self.config_data:
            self.config_data["misc"] = {}
        self.config_data["misc"]["angler_location"] = self.angler_location
        self.save_config_file(self.config_data)

    def _update_ocr_backend(self):
        self.ocr_backend = self.backend_var.get()
        self.ocr_engine = self.ocr_engine_tesseract if self.ocr_backend == "tesseract" else self.ocr_engine_winrt
        self.config_data["ocr"]["backend"] = self.ocr_backend
        self.save_config_file(self.config_data)

    def _update_overlay(self):
        self.enable_overlay = self.overlay_var.get()
        if self.enable_overlay:
            self.show_status_window()
        else:
            self.hide_status_window()
        if "ui" not in self.config_data:
            self.config_data["ui"] = {}
        self.config_data["ui"]["enable_overlay"] = self.enable_overlay
        self.save_config_file(self.config_data)

    def _update_debug(self):
        self.enable_debug = self.debug_var.get()
        if self.enable_debug:
            self.debug_window.show()
        else:
            self.debug_window.hide()
        if "ui" not in self.config_data:
            self.config_data["ui"] = {}
        self.config_data["ui"]["enable_debug"] = self.enable_debug
        self.save_config_file(self.config_data)

    def _update_delay_val(self, key, var_name, attr_name):
        try:
            val = float(getattr(self, var_name).get())
            setattr(self, attr_name, val)
            if "delay" not in self.config_data:
                self.config_data["delay"] = {}
            self.config_data["delay"][key] = val
            self.save_config_file(self.config_data)
        except ValueError:
            pass

    def _update_loop_delay(self):
        self._update_delay_val("loop", "loop_delay_var", "loop_delay")

    def _update_initial_delay(self):
        self._update_delay_val("initial", "initial_delay_var", "initial_delay")

    def _update_typing_delay(self):
        self._update_delay_val("typing", "typing_delay_var", "typing_delay")

    def _update_inv_delay(self):
        self._update_delay_val("inv", "inv_delay_var", "inv_delay")

    def _update_action_delay(self):
        self._update_delay_val("action", "action_delay_var", "action_delay")

    def sleep_interruptible(self, seconds):
        """Sleep for a duration but check for active/stop events periodically."""
        start_time = time.time()
        while time.time() - start_time < seconds:
            if self.force_stop.is_set():
                return False
            if not self.active.is_set():
                return False
            time.sleep(0.1)
        return True

    def angler_worker(self):
        self.log(f"Worker started. Location: {self.angler_location}")
        while not self.force_stop.is_set():
            self.active.wait()
            self.log("Starting quest loop...")

            try:
                # 1. Initial interaction (Press E)
                if not self.sleep_interruptible(self.initial_delay): continue
                self.log("Interacting (Pressing E)...")
                pydirectinput.press('e')
                
                # 2. Open dialogue
                if not self.sleep_interruptible(self.action_delay): continue
                self.log(f"Moving to dialogue: ({int(self.dialogue_x)}, {int(self.dialogue_y)})")
                pydirectinput.moveTo(int(self.dialogue_x), int(self.dialogue_y))
                if not self.sleep_interruptible(self.action_delay / 2): continue
                pydirectinput.moveTo(int(self.dialogue_x-1), int(self.dialogue_y))
                if not self.sleep_interruptible(self.action_delay): continue
                pydirectinput.click()
                if not self.sleep_interruptible(self.action_delay): continue
                pydirectinput.click()

                # 3. Capture and OCR
                if not self.sleep_interruptible(self.action_delay * 4): continue
                self.log("Capturing screen region...")
                frame = self.capture_screen()
                if frame is None:
                    self.log("Capture failed (box out of bounds?).")
                    if not self.sleep_interruptible(self.loop_delay): continue
                    continue
                
                self.log("Running OCR...")
                text = asyncio.run(self.read_frame(frame))
                if not text or not text.strip():
                    self.log("No text detected in capture region.")
                    if not self.sleep_interruptible(self.loop_delay): continue
                    continue
                
                # 4. Match Fish
                self.log(f"OCR Result: '{text.strip()}'")
                fish_list = self.config_data.get("fish_list", {}).get(self.angler_location, [])
                if not fish_list:
                    self.log(f"No fish list found for location: {self.angler_location}")
                    if not self.sleep_interruptible(self.loop_delay): continue
                    continue
                
                match = self.fuzzy_match(text, fish_list)
                if not match:
                    self.log("No confident match found in fish list.")
                    if not self.sleep_interruptible(self.loop_delay): continue
                    continue

                pydirectinput.moveTo(int(self.search_bar_x), int(self.search_bar_y))

                if not self.sleep_interruptible(self.action_delay / 2): continue
                pydirectinput.moveTo(int(self.search_bar_x-1), int(self.search_bar_y))

                if not self.sleep_interruptible(self.action_delay): continue

                self.log(f"Matched: {match}. Proceeding to turn in.")

                # 5. Inventory and Turn-in
                pydirectinput.press('g')
                if not self.sleep_interruptible(self.inv_delay): continue

                if not (self.last_fish is not None and self.last_fish == match):
                    self.log(f"Searching for {match}...")
                    if not self.sleep_interruptible(self.action_delay): continue
                    pydirectinput.click()
                    if not self.sleep_interruptible(self.action_delay): continue
                    pydirectinput.keyDown('ctrl')
                    pydirectinput.press('a')
                    pydirectinput.keyUp('ctrl')
                    pydirectinput.press('delete')
                    if not self.sleep_interruptible(self.action_delay): continue
                    pydirectinput.typewrite(match.lower(), interval=self.typing_delay)
                else:
                    self.log("Skipping search because it's the same fish as previous quest.")

                if not self.sleep_interruptible(self.action_delay): continue
                self.log("Selecting fish...")
                pydirectinput.moveTo(int(self.fish_area_x), int(self.fish_area_y))
                if not self.sleep_interruptible(self.action_delay / 2): continue
                pydirectinput.moveTo(int(self.fish_area_x-1), int(self.fish_area_y))
                if not self.sleep_interruptible(self.action_delay): continue
                pydirectinput.click()
                
                if not self.sleep_interruptible(self.action_delay): continue
                self.log("Closing interface...")
                pydirectinput.press('g')

                if not self.sleep_interruptible(self.action_delay): continue
                pydirectinput.press('e')
                
                if not self.sleep_interruptible(self.action_delay): continue
                pydirectinput.moveTo(int(self.dialogue_x), int(self.dialogue_y))
                if not self.sleep_interruptible(self.action_delay / 2): continue
                pydirectinput.moveTo(int(self.dialogue_x-1), int(self.dialogue_y))
                if not self.sleep_interruptible(self.action_delay): continue
                pydirectinput.click()

                if not self.sleep_interruptible(self.action_delay * 2): continue
                pydirectinput.press('1')
                if not self.sleep_interruptible(self.action_delay / 2): continue
                pydirectinput.press('1')

                self.last_fish = match
                self.log(f"Loop complete. Waiting {self.loop_delay}s...")
                if not self.sleep_interruptible(self.loop_delay): continue
                
            except Exception as e:
                self.log(f"Worker Error: {e}")
                if not self.sleep_interruptible(self.loop_delay): continue

    def run(self):
        self.capture_box.geometry(f"{self.capture_box.capture_width}x{self.capture_box.capture_height}+{self.capture_box.capture_x}+{self.capture_box.capture_y}")
        self.capture_box.withdraw()
        
        threading.Thread(target=self.angler_worker, daemon=True).start()
        self.mainloop()
