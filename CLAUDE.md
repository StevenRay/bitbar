# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Bitcoin menu bar application for macOS that displays real-time Bitcoin price data from the CoinGecko API. Built with Python using RUMPS (Ridiculously Uncomplicated macOS Python Statusbar apps) and PyObjC for native macOS integration.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode
python menu_bar_app.py

# Build standalone macOS app bundle
python setup.py py2app

# Clean build artifacts before rebuilding
rm -rf build dist
```

Built app appears in `dist/` directory as `Bitcoin Menu Bar App.app`.

## Architecture

### Core Components

**menu_bar_app.py** - Main application with three key classes:

1. **PopoverController** (NSObject)
   - Manages WKWebView popover interface
   - Handles JavaScript-to-Python bridge via `WKUserContentController`
   - Injected `window.pyObj` JavaScript object enables bi-directional communication
   - Message actions: `changeCurrency`, `updatePrice`, `openWebsite`, `openAbout`
   - Popover dimensions: 320x480px

2. **MenuBarApp** (rumps.App)
   - Menu bar status item with Bitcoin icon
   - Auto-updates price every 60 seconds via `rumps.Timer`
   - Title format: `₿ {symbol}{price} {arrow}{change}%`
   - Manages currency state (USD, EUR, GBP, JPY, CAD, AUD)
   - Threaded API requests to prevent UI blocking

3. **UI Integration**
   - Menu bar click opens popover (not dropdown menu)
   - `setup_popover()` overrides default rumps menu behavior by removing the menu and setting custom click action
   - Uses PyObjC's `AppHelper.callAfter()` for thread-safe UI updates from background threads

### UI Layer

**ui/index.html** - Embedded WKWebView content:
- Self-contained HTML/CSS/JS (no external dependencies)
- Displays: current price, 24h change, high/low, market cap, volume
- Currency switcher grid (6 currencies)
- Dark/light theme toggle
- Communicates with Python via injected `window.pyObj` bridge

### Data Flow

1. Timer triggers `update_price()` → spawns thread → `_fetch_price()`
2. Fetches from CoinGecko: `https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&ids=bitcoin`
3. `_update_ui(data)` uses `AppHelper.callAfter()` to update on main thread
4. Updates both menu bar title and WebView via JavaScript: `updateData({json_data})`
5. JavaScript bridge allows user interactions to trigger Python methods

### Build Configuration

**setup.py** - py2app configuration:
- Packages: rumps, requests (explicitly included)
- `DATA_FILES`: includes `ui/` directory
- `LSUIElement: True` - runs as menu bar app without dock icon
- Icon: `bitcoin_tracker_icon.icns`
- Bundle ID: `com.defendersoftheinternet.bitcoinmenubar`

## Key Technical Details

- **Threading**: All API calls run in background threads to prevent UI freezing
- **Thread Safety**: `PyObjCTools.AppHelper.callAfter()` ensures UI updates happen on main thread
- **PyObjC Bridge**: Direct access to Cocoa APIs (NSPopover, WKWebView, NSStatusBar)
- **RUMPS Override**: Custom popover replaces standard rumps dropdown menu by accessing underlying NSStatusItem
- **No External UI Dependencies**: WebView uses vanilla HTML/CSS/JS only

## API Integration

CoinGecko API (public, no key required):
- Endpoint: `/api/v3/coins/markets`
- Parameters: `vs_currency`, `ids=bitcoin`
- Returns: current_price, price_change_percentage_24h, high_24h, low_24h, market_cap, total_volume
- Timeout: 10 seconds
