from .config import Config
from .ui_helpers import UIHelpers
from .capture_helpers import CaptureHelpers
from .hotkey_helpers import HotkeyHelpers
from .ocr_handler import OcrHandler
from .coordinates_helpers import CoordinatesHelpers
from .test_helpers import TestHelpers
from .uinput_handler import UInputHandler

class Utils(Config, UIHelpers, CaptureHelpers, HotkeyHelpers, OcrHandler, CoordinatesHelpers, TestHelpers, UInputHandler):
    pass
