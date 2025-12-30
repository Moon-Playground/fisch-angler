import cv2


class CaptureHelpers:
    def capture_screen_region(self):
        """
        Capture a specific region of the screen using dxcam.
        
        Returns:
            numpy.ndarray or None: The captured frame, or None if capture failed
        """
        if self.camera is None:
            return None

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int(self.capture_box.capture_x)
        y = int(self.capture_box.capture_y)
        w = int(self.capture_box.capture_width)
        h = int(self.capture_box.capture_height)

        left = max(0, x)
        top = max(0, y)
        right = min(screen_width, x + w)
        bottom = min(screen_height, y + h)

        if right <= left or bottom <= top:
            return None

        try:
            frame = self.camera.grab(region=(left, top, right, bottom))
            return frame
        except Exception as e:
            # print(f"Capture error: {e}")
            return None
