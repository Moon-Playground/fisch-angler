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
- 🕹️ **Customizable Hotkeys**: Take full control with user-defined hotkeys for all major actions.
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

### Prebuilt binaries
1. Download the latest release from [releases](https://github.com/Moon-Playground/fisch-angler/releases).
2. Extract the contents of the downloaded zip file.
3. Run `angler.exe`.

### from source
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Moon-Playground/fisch-angler.git
   cd fisch-angler
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Configuration**:
   The application will automatically generate a default `auto_shake.toml` upon the first launch.

---

## 🚀 Usage

WIP

### ⌨️ Default Hotkeys

| Action | Key | Description |
| :--- | :--- | :--- |
| **Test Capture** | `F2` | Captures the current region and displays OCR results. |
| **Toggle Box** | `F3` | Shows or hides the capture region selection box. |
| **Toggle Action** | `F4` | Starts or stops the automation worker. |
| **Exit App** | `F5` | Gracefully closes the application. |

### 🎯 Setting Up

1. **Position the Capture Box**: Press `F3` and drag/resize the blue box over the area where fish names appear.
2. **Set Click Points**: Use the "Set Coordinates" buttons in the UI to define where the app should click (Search Bar, Dialogue, etc.).
3. **Select Location**: Choose your current in-game location from the dropdown to load the corresponding fish list.
4. **Start**: Press `F4` to begin automation.

---

## ⚙️ Configuration

Settings are persisted in `auto_shake.toml`. You can manually edit this file to fine-tune delays, add new fish, or change hotkeys.

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
