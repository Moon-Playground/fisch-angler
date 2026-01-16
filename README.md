# 🎣 Angler Quest Automation

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

Macro for automating angler quest in Roblox fisch.

---

## ✨ Features

- 🚀 **High-Speed Capture**: Powered by `dxcam-cpp`, achieving ultra-low latency screen region monitoring.
- 🔍 **Dual OCR Backends**: 
  - **Tesseract OCR**: Industry-standard open-source OCR engine.
  - **Windows WinRT OCR**: Native, hardware-accelerated OCR for Windows.
- 🎯 **Fuzzy Matching**: Intelligent text recognition that compensates for OCR inaccuracies using `rapidfuzz`.
- 🕹️ **Low-Level Input**: Uses `pydirectinput-rgx` for better game compatibility.
- 🎨 **Modern Interface**: A sleek, dark-themed dashboard built with `CustomTkinter`.
- 🌍 **Multi-Location Support**: Built-in configurations for many in-game locations (Moosewood, Sunstone, Roslit, etc.).
- 📊 **Real-time Debugging**: Transparent overlay and detailed log window for real-time status tracking.

---

## 🛠️ Prerequisites

- **Python 3.11 or higher**
- **Windows 10/11** (Required for WinRT and DXCam)
- **Tesseract OCR** (Recommended): 
  - Install from [here](https://github.com/UB-Mannheim/tesseract/wiki).
  - Default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

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
backend = "tesseract" # or "winrt"

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
