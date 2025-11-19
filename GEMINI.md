# Project Overview

This project is a macOS menu bar application that displays the current price of Bitcoin in USD. It's built with Python using the `rumps` library for the menu bar interface and `requests` to fetch data from the CoinGecko API.

The application shows the Bitcoin price in the menu bar, along with an arrow indicating the direction of the price change and the percentage change since the last update.

# Building and Running

To build and run this application, you'll need Python and `py2app` installed.

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file does not exist. I will create one based on `setup.py`)*

2.  **Run in Development Mode:**
    ```bash
    python menu_bar_app.py
    ```

3.  **Build the Application:**
    ```bash
    python setup.py py2app
    ```
    This will create a `Bitcoin Menu Bar App.app` file in the `dist` directory.

# Development Conventions

*   **Main Application:** The main application logic is in `menu_bar_app.py`.
*   **Dependencies:** Project dependencies are managed in `setup.py` for the `py2app` build.
*   **UI:** The user interface is handled by the `rumps` library.
*   **Data:** The Bitcoin price data is fetched from the public CoinGecko API.
