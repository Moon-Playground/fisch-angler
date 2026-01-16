import os
import sys


class UIHelpers:
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller/Nuitka """
        if getattr(sys, 'frozen', False):
            # If frozen (PyInstaller, Nuitka, cx_Freeze)
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller and some Nuitka configurations
                base_path = sys._MEIPASS
            else:
                # Nuitka onefile/standalone fallback
                # This file is deep in angler/utils/ui_helpers.py
                # We need to go up 3 levels to reach the root where 'res' exists
                current_dir = os.path.dirname(os.path.abspath(__file__))
                base_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
        else:
            # Development: use the directory of the package
            # This file is in angler/utils, so the package root is one level up
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_path, relative_path)

        # Fallback to CWD if not found, for backward compatibility
        if not os.path.exists(full_path):
            cwd_path = os.path.join(os.path.abspath("."), relative_path)
            if os.path.exists(cwd_path):
                return cwd_path
        return full_path

    def find_and_set_icon(self):
        """
        Find and set the application icon from various candidate paths.
        
        Returns:
            bool: True if icon was successfully set, False otherwise
        """
        icon_path = self.resource_path("res/icon.ico")
        try:
            self.iconbitmap(icon_path)
            return True
        except Exception:
            return False
