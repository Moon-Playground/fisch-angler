import asyncio
import cv2
import sys
import os

from rapidfuzz import process
import numpy as np


class OcrHandler:
    def test_tesseract(self):
        try:
            import pytesseract
        except ImportError:
            return False
        else:
            try:
                version = pytesseract.get_tesseract_version()
                return True
            except Exception:
                return False

    def init_ocr_engine_tesseract(self):
        try:
            import pytesseract
            return pytesseract
        except Exception as e:
            print(f"Error initializing Tesseract: {e}")
            return None

    def init_ocr_engine_winrt(self):
        return None

    async def recognize_frame(self, ocr_engine, frame):
        return await self.recognize_frame_tesseract(ocr_engine, frame)

    async def recognize_frame_tesseract(self, ocr_engine, frame):
        if ocr_engine is None:
            return ""
        try:
            processed_frame = self.process_image(frame)
            result = ocr_engine.image_to_string(processed_frame)
            return result
        except Exception as e:
            print(f"Error recognizing frame with Tesseract: {e}")
            return ""

    async def recognize_frame_winrt(self, ocr_engine, frame):
        return ""

    def fuzzy_match(self, text, target, threshold=60):
        if not text or not text.strip():
            return None
        result = process.extractOne(text, target)
        if result and result[1] >= threshold:
            return result[0]
        return None

    async def read_frame(self, frame):
        return await self.recognize_frame(self.ocr_engine, frame)

    def process_image(self, image):
        """
        Process image to highlight white text for better OCR.
        Expects RGB numpy array (from mss).
        Returns a processed numpy array (grayscale/binary).
        """
        # mss returns RGB
        frame_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # --- Improvement for Small Text ---
        
        # 1. Upscale the image
        scale_factor = 3
        height, width = frame_bgr.shape[:2]
        img = cv2.resize(frame_bgr, (width * scale_factor, height * scale_factor), interpolation=cv2.INTER_CUBIC)
        
        # 2. Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 3. Sharpen the image
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        gray = cv2.filter2D(gray, -1, sharpen_kernel)
        
        # 4. Threshold to get white text
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        
        # 5. Optional: Morphological closing
        kernel = np.ones((2,2), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return thresh
