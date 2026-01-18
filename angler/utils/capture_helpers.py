import cv2
import numpy as np


class CaptureHelpers:
    def capture_screen_region(self):
        """
        Capture a specific region of the screen using mss.
        
        Returns:
            numpy.ndarray or None: The captured frame, or None if capture failed
        """
        if self.camera is None:
            return None

        x = int(self.capture_box.capture_x)
        y = int(self.capture_box.capture_y)
        w = int(self.capture_box.capture_width)
        h = int(self.capture_box.capture_height)

        try:
            # mss uses monitor={"top": y, "left": x, "width": w, "height": h}
            monitor = {"top": y, "left": x, "width": w, "height": h}
            sct_img = self.camera.grab(monitor)
            frame = np.array(sct_img)
            # Convert BGRA to RGB for consistency
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            return frame
        except Exception as e:
            # print(f"Capture error: {e}")
            return None
