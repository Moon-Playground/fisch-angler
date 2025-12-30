import os
import sys


class UIHelpers:
    def find_and_set_icon(self):
        """
        Find and set the application icon from various candidate paths.
        
        Returns:
            bool: True if icon was successfully set, False otherwise
        """
        icon_candidates = []
        
        # 1. PyInstaller Temp Path
        if hasattr(sys, '_MEIPASS'):
            icon_candidates.append(os.path.join(sys._MEIPASS, "res", "icon.ico"))
            icon_candidates.append(os.path.join(sys._MEIPASS, "icon.ico"))
        
        # 2. Local Paths
        icon_candidates.append(os.path.abspath("res/icon.ico"))
        icon_candidates.append(os.path.abspath("icon.ico"))

        for icon_path in icon_candidates:
            if os.path.exists(icon_path):
                try:
                    self.iconbitmap(icon_path)
                    return True
                except Exception:
                    continue
        
        return False
