import keyboard
import pydirectinput
import time
from tkinter import messagebox

class CoordinatesHelpers:
    def _wait_for_pos(self, label):
        messagebox.showinfo("Selection", f"Put the mouse over {label} then press R to set.")
        
        # Wait for 'R' key while keeping GUI responsive
        while True:
            if keyboard.is_pressed('r'):
                break
            try:
                self.update()
            except:
                break
            time.sleep(0.01)
            
        x, y = pydirectinput.position()
        messagebox.showinfo("Success", f"{label} coordinates set: {x}, {y}")
        return x, y

    def select_fish_area(self):
        x, y = self._wait_for_pos("Fish Area")
        self.fish_area_x = x
        self.fish_area_y = y
        self.fish_area_var.set(f"x: {x}, y: {y}")
        self.log(f"Fish Area set to: ({x}, {y})")
        self.save_config_coords()

    def select_search_bar(self):
        x, y = self._wait_for_pos("Search Bar")
        self.search_bar_x = x
        self.search_bar_y = y
        self.search_bar_var.set(f"x: {x}, y: {y}")
        self.log(f"Search Bar set to: ({x}, {y})")
        self.save_config_coords()

    def select_dialogue(self):
        x, y = self._wait_for_pos("Dialogue")
        self.dialogue_x = x
        self.dialogue_y = y
        self.dialogue_var.set(f"x: {x}, y: {y}")
        self.log(f"Dialogue set to: ({x}, {y})")
        self.save_config_coords()
