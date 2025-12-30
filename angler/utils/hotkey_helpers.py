import keyboard as kb


class HotkeyHelpers:
    def cleanup_hotkeys(self, hotkey_list):
        """
        Remove all hotkeys from the given list.
        
        Args:
            hotkey_list: List of hotkey strings to remove
        """
        for hk in hotkey_list:
            try:
                kb.remove_hotkey(hk)
            except:
                pass

    def register_hotkey(self, hotkey_string, callback):
        """
        Register a single hotkey with error handling.
        
        Args:
            hotkey_string: The hotkey combination string (e.g., "F3", "ctrl+shift+a")
            callback: The function to call when the hotkey is pressed
            
        Returns:
            bool: True if registration succeeded, False otherwise
        """
        if not hotkey_string:
            return False
        
        try:
            kb.add_hotkey(hotkey_string, callback)
            return True
        except Exception as e:
            print(f"Failed to register hotkey {hotkey_string}: {e}")
            return False

    def apply_hotkeys(self):
        """
        Apply hotkeys from configuration.
        """
        # Clean up existing hotkeys
        if hasattr(self, 'active_hotkeys'):
            self.cleanup_hotkeys(self.active_hotkeys)
        
        self.active_hotkeys = []

        # Get hotkey configuration
        t_test = self.config_data["hotkeys"].get("test_capture", "F2")
        t_box = self.config_data["hotkeys"].get("toggle_box", "F3")
        t_act = self.config_data["hotkeys"].get("toggle_action", "F4")
        t_exit = self.config_data["hotkeys"].get("exit_app", "F5")

        # Register hotkeys
        hotkey_map = [
            (t_test, "<<TestCapture>>"),
            (t_box, "<<ToggleBox>>"),
            (t_act, "<<ToggleAction>>"),
            (t_exit, "<<ExitApp>>")
        ]
        
        for hk, event_name in hotkey_map:
            if self.register_hotkey(hk, lambda e=event_name: self.after(0, self.event_generate, e)):
                self.active_hotkeys.append(hk)

        # Update info label
        self.info_label.configure(text=f"{t_test}: Test Capture | {t_box}: Toggle Capture Box | {t_act}: Start/Stop | {t_exit}: Exit")
