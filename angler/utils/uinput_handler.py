import uinput
import time
import mss

class UInputHandler:
    def __init__(self):
        self.device = None
        self.key_map = {}
        self.screen_width = 1920
        self.screen_height = 1080
        self._init_device()

    def _init_device(self):
        """Initialize the virtual uinput device."""
        try:
            # Get screen resolution for absolute coordinates
            with mss.mss() as sct:
                monitor = sct.monitors[0]
                self.screen_width = monitor['width']
                self.screen_height = monitor['height']

            events = [
                uinput.BTN_LEFT,
                uinput.BTN_RIGHT,
                uinput.ABS_X + (0, self.screen_width, 0, 0),
                uinput.ABS_Y + (0, self.screen_height, 0, 0),
            ]

            # Basic key mapping for common keys
            self.key_map = {
                'e': uinput.KEY_E,
                'g': uinput.KEY_G,
                '1': uinput.KEY_1,
                'ctrl': uinput.KEY_LEFTCTRL,
                'control': uinput.KEY_LEFTCTRL,
                'a': uinput.KEY_A,
                'delete': uinput.KEY_DELETE,
                'space': uinput.KEY_SPACE,
                'enter': uinput.KEY_ENTER,
                'backspace': uinput.KEY_BACKSPACE,
                'shift': uinput.KEY_LEFTSHIFT,
                'esc': uinput.KEY_ESC,
                'tab': uinput.KEY_TAB,
            }

            # Add numeric keys 0-9
            for i in range(10):
                self.key_map[str(i)] = getattr(uinput, f"KEY_{i}")

            # Add alphabet keys a-z
            for char in "abcdefghijklmnopqrstuvwxyz":
                self.key_map[char] = getattr(uinput, f"KEY_{char.upper()}")

            # Add common symbols
            self.key_map[' '] = uinput.KEY_SPACE
            self.key_map['-'] = uinput.KEY_MINUS
            self.key_map['.'] = uinput.KEY_DOT
            self.key_map[','] = uinput.KEY_COMMA
            self.key_map['/'] = uinput.KEY_SLASH
            self.key_map['\\'] = uinput.KEY_BACKSLASH
            self.key_map['['] = uinput.KEY_LEFTBRACE
            self.key_map[']'] = uinput.KEY_RIGHTBRACE
            self.key_map[';'] = uinput.KEY_SEMICOLON
            self.key_map["'"] = uinput.KEY_APOSTROPHE
            self.key_map['='] = uinput.KEY_EQUAL
            self.key_map['`'] = uinput.KEY_GRAVE

            # Combine all events
            all_events = events + list(set(self.key_map.values()))
            self.device = uinput.Device(all_events, name="angler-virtual-input")
            
            # Small delay to ensure device is registered by the system
            time.sleep(1)
        except Exception as e:
            print(f"Error initializing uinput device: {e}")
            print("Make sure you have permissions to /dev/uinput or run as root.")

    def press(self, key):
        """Press and release a key."""
        if not self.device: return
        key_code = self.key_map.get(key.lower())
        if key_code:
            self.device.emit_click(key_code)

    def keyDown(self, key):
        """Hold a key down."""
        if not self.device: return
        key_code = self.key_map.get(key.lower())
        if key_code:
            self.device.emit(key_code, 1)

    def keyUp(self, key):
        """Release a key."""
        if not self.device: return
        key_code = self.key_map.get(key.lower())
        if key_code:
            self.device.emit(key_code, 0)

    def moveTo(self, x, y):
        """Move the mouse to absolute coordinates."""
        if not self.device: return
        # Ensure coordinates are within screen bounds
        x = max(0, min(int(x), self.screen_width))
        y = max(0, min(int(y), self.screen_height))
        self.device.emit(uinput.ABS_X, x, syn=False)
        self.device.emit(uinput.ABS_Y, y)

    def click(self, x=None, y=None):
        """Click the left mouse button at current or specified position."""
        if not self.device: return
        if x is not None and y is not None:
            self.moveTo(x, y)
        self.device.emit_click(uinput.BTN_LEFT)

    def typewrite(self, text, interval=0.0):
        """Type a string of characters."""
        if not self.device: return
        for char in text:
            self.press(char)
            if interval > 0:
                time.sleep(interval)
