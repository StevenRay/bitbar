# Bitbar ₿

A beautiful, native-feeling Bitcoin price tracker for your macOS menu bar.

**Bitbar** sits quietly in your menu bar, displaying the live Bitcoin price and 24h trend. One click opens a stunning, glass-morphic dashboard with detailed stats, currency conversion, and more.

## ✨ Features

*   **Live Price Updates**: Real-time Bitcoin price in your menu bar.
*   **Rich Menu Bar Widget**: Color-coded trend indicators (Green/Red) and custom typography.
*   **Beautiful Dashboard**: A modern, glass-morphic UI built with HTML/CSS/JS running in a native popover.
*   **Multi-Currency Support**: Switch instantly between USD, EUR, GBP, JPY, CAD, AUD, KRW, BRL, and TRY.
*   **Dark Mode**: Fully themed for both Light and Dark macOS appearances.
*   **Detailed Stats**: View 24h High/Low, Market Cap, and Volume.
*   **Native Feel**: Blurs the background behind the popover for that premium macOS aesthetic.

## 🚀 Installation

1.  Download the latest release (coming soon).
2.  Drag **Bitbar.app** to your Applications folder.
3.  Launch and enjoy!

## 🛠️ Development

### Prerequisites

*   Python 3.x
*   macOS (Required for `rumps` and `pyobjc`)

### Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/StevenRay/bitbar.git
    cd bitbar
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run locally:
    ```bash
    python3 menu_bar_app.py
    ```

### Building the App

To create a standalone `.app` bundle:

```bash
python3 setup.py py2app
```

The compiled application will be in the `dist/` directory.

## 🏗️ Tech Stack

*   **Python**: Core application logic.
*   **Rumps**: macOS menu bar integration.
*   **PyObjC**: Native macOS API bridge (Cocoa, WebKit).
*   **WKWebView**: Rendering the modern HTML/CSS interface.
*   **CoinGecko API**: Free, reliable cryptocurrency data.

## ❤️ Credits

Made with ❤️ by **Stoodio™**.
