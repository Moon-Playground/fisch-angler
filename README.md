# 🎣 Angler Quest Automation (Linux Branch)

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://github.com/Moon-Playground/fisch-angler)

**Note: This is the Linux-specific branch of the Angler macro.** For the Windows version, please refer to the `main` branch.

---

## ✨ Features

- 🚀 **High-Speed Capture**: Powered by `mss`, achieving low latency screen region monitoring.
- 🔍 **OCR Engine**: Standardized on **Tesseract OCR** for reliable text recognition.
- 🎯 **Fuzzy Matching**: Intelligent text recognition that compensates for OCR inaccuracies using `rapidfuzz`.
- 🕹️ **Low-Level Input**: Uses `pyautogui` for game compatibility.
- ⌨️ **Hotkeys**: Uses `pynput` for root-less hotkey support on X11.
- 🎨 **Modern Interface**: A sleek, dark-themed dashboard built with `CustomTkinter`.
- 🌍 **Multi-Location Support**: Built-in configurations for many in-game locations (Moosewood, Sunstone, Roslit, etc.).
- 📊 **Real-time Debugging**: Transparent overlay and detailed log window for real-time status tracking.

---

## 🛠️ Prerequisites

- **Python 3.11 or higher**
- **Tesseract OCR**: Install via your package manager (e.g., `sudo apt install tesseract-ocr`).
- **X11 Session (Linux)**: This macro currently **does not support Wayland**. Most Linux distributions (like Ubuntu, Fedora, Debian) default to Wayland. You must switch to an **Xorg/X11** session at the login screen for screen capture and hotkeys to work.

---

## 📦 Installation

### Prebuilt Binaries
1. Download the latest release from [Releases](https://github.com/Moon-Playground/fisch-angler/releases).
2. Extract the ZIP file.
3. Run `angler.exe`.

### From Source
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Moon-Playground/fisch-angler.git
   cd fisch-angler
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

For a detailed step-by-step setup guide with images, please refer to the **[USAGE.md](./USAGE.md)**.

### Quick Start:
1. **Set Location**: Choose your current area on the Home tab.
2. **Configure OCR**: Press `F3` to position the capture box over the fish name.
3. **Set Coordinates**: Use the "Coordinates" tab to pick click points (Dialogue, Search Bar, etc.).
4. **Run**: Press `F4` to start/stop the macro.

### ⌨️ Default Hotkeys

| Action | Key | Description |
| :--- | :--- | :--- |
| **Test Capture** | `F2` | Runs OCR on the current region and shows result. |
| **Toggle Box** | `F3` | Shows/Hides the capture region selection box. |
| **Start/Stop** | `F4` | Starts or stops the automation worker. |
| **Exit App** | `F5` | Gracefully closes the application. |

---

## ⚙️ Configuration

Settings are persisted in `angler.toml`. You can manually edit this file to fine-tune delays, add new fish, or change hotkeys.

```toml
[ocr]
capture_width = 124

[delay]
loop = 30.0    # Cycle delay in seconds
action = 0.5   # Delay between simulated actions
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
