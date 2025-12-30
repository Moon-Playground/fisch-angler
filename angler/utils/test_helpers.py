import customtkinter as ctk
from PIL import Image
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams
import cv2
import numpy as np

class TestHelpers:
    def show_capture_dialog(self, frame=None, text=None):
        top = ctk.CTkToplevel(self)
        top.title("Captured Image")
        # Lift window
        top.attributes("-topmost", True)

        if frame is None:
            lbl_text = ctk.CTkLabel(top, text=text, wraplength=350)
            lbl_text.pack(padx=20, pady=(0, 20))
            return

        # Process frame to see what OCR sees
        processed_frame = self.process_image(frame)
        
        # Convert numpy array to PIL Image for CTkImage
        # processed_frame is expected to be a numpy array (grayscale/binary)
        if isinstance(processed_frame, np.ndarray):
            img = Image.fromarray(processed_frame)
        else:
            # Fallback if process_image returned something else (e.g. SoftwareBitmap)
            img = Image.new("RGB", (100, 100), "gray")

        lbl_text = ctk.CTkLabel(top, text=f"OCR Backend: {getattr(self, 'ocr_backend', 'Unknown')}", wraplength=350)
        lbl_text.pack(padx=20, pady=(0, 0))
        
        # Create CTkImage - keeping original size
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        
        lbl_img = ctk.CTkLabel(top, text="", image=ctk_img)
        lbl_img.pack(padx=20, pady=20)
        
        lbl_text = ctk.CTkLabel(top, text=f"OCR Result:\n{text}", wraplength=350)
        lbl_text.pack(padx=20, pady=(0, 20))

        # Check if we have angler_location and fuzzy_match
        target_list = self.config_data.get("fish_list", {}).get(self.angler_location, [])
        if target_list:
            fuzzy_result = self.fuzzy_match(text, target_list)
            lbl_text = ctk.CTkLabel(top, text=f"Fuzzy Result:\n{fuzzy_result}", wraplength=350)
            lbl_text.pack(padx=20, pady=(0, 20))
