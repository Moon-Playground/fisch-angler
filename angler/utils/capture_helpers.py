import cv2
import numpy as np
import mss
import threading


class CaptureHelpers:
    @property
    def camera(self):
        """Get or create a thread-local mss instance."""
        if not hasattr(self, '_mss_local'):
            self._mss_local = threading.local()
        if not hasattr(self._mss_local, 'instance'):
            try:
                self._mss_local.instance = mss.mss()
            except Exception as e:
                # Fallback or log if mss fails to init in this thread
                return None
        return self._mss_local.instance

    def capture_screen_region(self):
        """
        Capture a specific region of the screen using mss.
        
        Returns:
            numpy.ndarray or None: The captured frame, or None if capture failed
        """
        try:
            # Get the thread-local camera
            camera = self.camera
            if camera is None or not camera.monitors:
                self.log("Capture error: No monitors detected by mss. Check X11/Wayland compatibility.")
                return None

            x = int(self.capture_box.capture_x)
            y = int(self.capture_box.capture_y)
            w = int(self.capture_box.capture_width)
            h = int(self.capture_box.capture_height)

            # Get screen bounds to prevent out-of-bounds errors
            # monitors[0] is the virtual screen (all monitors combined)
            screen = camera.monitors[0]
            screen_left = screen["left"]
            screen_top = screen["top"]
            screen_width = screen["width"]
            screen_height = screen["height"]

            # Clamp the coordinates and size
            left = max(screen_left, x)
            top = max(screen_top, y)
            
            # Adjust width/height if they go beyond screen edges
            right = min(screen_left + screen_width, x + w)
            bottom = min(screen_top + screen_height, y + h)
            
            width = right - left
            height = bottom - top

            if width <= 0 or height <= 0:
                self.log(f"Capture error: Box is off-screen or zero size (x:{x}, y:{y}, w:{w}, h:{h}) on screen (w:{screen_width}, h:{screen_height})")
                return None

            monitor = {"top": top, "left": left, "width": width, "height": height}
            sct_img = camera.grab(monitor)
            frame = np.array(sct_img)
            # Convert BGRA to RGB for consistency
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            return frame
        except Exception as e:
            self.log(f"Capture error exception: {e}")
            return None
