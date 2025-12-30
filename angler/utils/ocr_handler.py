import asyncio

import winrt.windows.media.ocr as ocr
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
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        
        # Threshold to get white text (adjust values if needed)
        # 200-255 range is usually good for white text
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        return thresh
