from pynput import keyboard
import threading

class HotkeyHelpers:
    def cleanup_hotkeys(self):
        """
        Stop the global hotkey listener if it exists.
        """
        if hasattr(self, 'hotkey_listener') and self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
            except:
                pass
            self.hotkey_listener = None

    def _to_pynput(self, hk_string):
        """
        Convert project hotkey strings (e.g., 'F2', 'ctrl+shift+a') 
        to pynput format (e.g., '<f2>', '<ctrl>+<shift>+a').
        """
        if not hk_string:
            return ""
            
        hk = hk_string.lower().replace(" ", "")
        
        # Mapping for special keys
        special_map = {
            'alt': '<alt>',
            'ctrl': '<ctrl>',
            'control': '<ctrl>',
            'shift': '<shift>',
            'win': '<win>',
            'windows': '<win>',
            'cmd': '<cmd>',
            'command': '<cmd>',
            'enter': '<enter>',
            'esc': '<esc>',
            'escape': '<esc>',
            'tab': '<tab>',
            'space': '<space>',
            'delete': '<delete>',
            'backspace': '<backspace>',
        }
        
        # Handle function keys F1-F12
        for i in range(1, 13):
            special_map[f'f{i}'] = f'<f{i}>'
            
        parts = hk.split('+')
        converted = []
        for p in parts:
            if p in special_map:
                converted.append(special_map[p])
            else:
                converted.append(p)
                
        return "+".join(converted)

    def apply_hotkeys(self):
        """
        Apply hotkeys from configuration using pynput.
        """
        # Clean up existing listener
        self.cleanup_hotkeys()

        # Get hotkey configuration
        t_test = self.config_data["hotkeys"].get("test_capture", "F2")
        t_box = self.config_data["hotkeys"].get("toggle_box", "F3")
        t_act = self.config_data["hotkeys"].get("toggle_action", "F4")
        t_exit = self.config_data["hotkeys"].get("exit_app", "F5")

        # Create callbacks that use self.after to run on the main thread (Tkinter requirement)
        def trigger(event_name):
            self.after(0, self.event_generate, event_name)

        # Map to pynput format
        hotkey_map = {
            self._to_pynput(t_test): lambda: trigger("<<TestCapture>>"),
            self._to_pynput(t_box): lambda: trigger("<<ToggleBox>>"),
            self._to_pynput(t_act): lambda: trigger("<<ToggleAction>>"),
            self._to_pynput(t_exit): lambda: trigger("<<ExitApp>>")
        }

        try:
            # Filter out empty hotkeys
            valid_hotkeys = {k: v for k, v in hotkey_map.items() if k}
            self.hotkey_listener = keyboard.GlobalHotKeys(valid_hotkeys)
            self.hotkey_listener.start()
            self.log("Global hotkeys initialized via pynput.")
        except Exception as e:
            self.log(f"Failed to start hotkey listener: {e}")
            print(f"Error starting pynput listener: {e}")

        # Update info label (use original strings for display)
        self.info_label.configure(text=f"{t_test}: Test Capture | {t_box}: Toggle Capture Box | {t_act}: Start/Stop | {t_exit}: Exit")
