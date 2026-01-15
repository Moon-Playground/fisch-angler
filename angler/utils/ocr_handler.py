import asyncio

import winrt.windows.media.ocr as ocr
import winrt.windows.foundation
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams
import cv2

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
                pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                version = pytesseract.get_tesseract_version()
                return True
            except Exception:
                return False

    def init_ocr_engine_tesseract(self):
        try:
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            return pytesseract
        except Exception as e:
            print(f"Error initializing Tesseract: {e}")
            return None

    def init_ocr_engine_winrt(self):
        try:
            return ocr.OcrEngine.try_create_from_user_profile_languages()
        except Exception as e:
            print(f"Error initializing WinRT OCR: {e}")
            return None

    async def recognize_frame(self, ocr_engine, frame):
        if self.ocr_backend == "tesseract":
            return await self.recognize_frame_tesseract(ocr_engine, frame)
        else:
            return await self.recognize_frame_winrt(ocr_engine, frame)

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
        if ocr_engine is None:
            return ""
        try:
            processed_frame = self.process_image(frame)
            
            # Encode to PNG for WinRT OCR stream
            success, img_encoded = cv2.imencode('.png', processed_frame)
            if not success:
                raise Exception("Failed to encode image")
            img_bytes = img_encoded.tobytes()

            # Write data to Windows RandomAccessStream
            stream = streams.InMemoryRandomAccessStream()
            writer = streams.DataWriter(stream.get_output_stream_at(0))
            writer.write_bytes(img_bytes)
            await writer.store_async()
            
            # Use BitmapDecoder to interpret the image
            decoder = await imaging.BitmapDecoder.create_async(stream)
            
            # Get SoftwareBitmap from decoder
            software_bitmap = await decoder.get_software_bitmap_async()
            
            # Recognize
            result = await ocr_engine.recognize_async(software_bitmap)
            return result.text
            
        except Exception as e:
            print(f"OCR Internal Error: {e}")
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
        Expects RGB numpy array (from dxcam) or SoftwareBitmap.
        Returns a processed numpy array (grayscale/binary).
        """
        if isinstance(image, imaging.SoftwareBitmap):
            # Handle SoftwareBitmap (MSS mode)
            width = image.pixel_width
            height = image.pixel_height
            
            # Copy to buffer
            buf_len = width * height * 4
            buf = streams.Buffer(buf_len)
            image.copy_to_buffer(buf)
            
            # Read bytes
            reader = streams.DataReader.from_buffer(buf)
            pixel_bytes = bytearray(buf_len)
            reader.read_bytes(pixel_bytes)
            
            # Create numpy array (MSS/WinRT is usually BGRA8)
            frame_bgra = np.frombuffer(pixel_bytes, dtype=np.uint8).reshape((height, width, 4))
            frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
        else:
            # dxcam returns RGB
            frame_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # --- Improvement for Small Text ---
        
        # 1. Upscale the image - OCR engines work better with larger text
        # Scaling by 2x or 3x is usually the sweet spot
        scale_factor = 3
        height, width = frame_bgr.shape[:2]
        img = cv2.resize(frame_bgr, (width * scale_factor, height * scale_factor), interpolation=cv2.INTER_CUBIC)
        
        # 2. Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 3. Sharpen the image to make edges crisper
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        gray = cv2.filter2D(gray, -1, sharpen_kernel)
        
        # 4. Threshold to get white text
        # Lowered threshold slightly to 180 (from 200) to capture more variants of white/light gray
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        
        # 5. Optional: Morphological closing to fill small gaps in characters
        kernel = np.ones((2,2), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return thresh
