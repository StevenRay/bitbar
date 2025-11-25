import rumps
import requests
import os
import sys
import json
import time
import threading
import webbrowser
import objc
from Cocoa import NSObject, NSPopover, NSPopoverBehaviorTransient, NSViewController, NSApplication, NSImage
from WebKit import WKWebView, WKWebViewConfiguration, WKUserContentController, WKUserScript, WKUserScriptInjectionTimeAtDocumentStart
from Foundation import NSURL, NSMakeRect
from PyObjCTools import AppHelper

# Constants
WEBSITE_URL = "http://www.defendersoftheinternet.com"
UPDATE_INTERVAL = 60  # seconds
DEBUG = False  # Set to True to enable debug logging

def debug_print(msg):
    """Print debug messages only when DEBUG is enabled"""
    if DEBUG:
        print(msg)

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller/py2app"""
    if getattr(sys, 'frozen', False):
        # Running as compiled app
        # The executable is in Contents/MacOS, resources are in Contents/Resources
        base_path = os.path.join(os.path.dirname(sys.executable), '..', 'Resources')
    else:
        # Running from source
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class PopoverController(NSObject):
    def initWithApp_(self, app):
        self = objc.super(PopoverController, self).init()
        if self:
            self.app = app
            self.popover = NSPopover.alloc().init()
            self.popover.setBehavior_(NSPopoverBehaviorTransient)
            
            # Create WebView
            config = WKWebViewConfiguration.alloc().init()
            user_content = WKUserContentController.alloc().init()
            
            # Inject bridge script
            script_source = """
            window.pyObj = {
                changeCurrency: function(c) { window.webkit.messageHandlers.controller.postMessage({action: 'changeCurrency', currency: c}); },
                updatePrice: function() { window.webkit.messageHandlers.controller.postMessage({action: 'updatePrice'}); },
                openWebsite: function() { window.webkit.messageHandlers.controller.postMessage({action: 'openWebsite'}); },
                openAbout: function() { window.webkit.messageHandlers.controller.postMessage({action: 'openAbout'}); },
                quitApp: function() { window.webkit.messageHandlers.controller.postMessage({action: 'quitApp'}); },
                resizeWindow: function(h) { window.webkit.messageHandlers.controller.postMessage({action: 'resizeWindow', height: h}); }
            };
            """
            user_script = WKUserScript.alloc().initWithSource_injectionTime_forMainFrameOnly_(
                script_source, WKUserScriptInjectionTimeAtDocumentStart, True
            )
            user_content.addUserScript_(user_script)
            user_content.addScriptMessageHandler_name_(self, "controller")
            config.setUserContentController_(user_content)
            
            self.webview = WKWebView.alloc().initWithFrame_configuration_(NSMakeRect(0, 0, 320, 600), config)
            
            # Load HTML
            # Load HTML
            html_path = get_resource_path(os.path.join("ui", "index.html"))
            # Add timestamp to force reload and bypass cache
            import time
            url = NSURL.fileURLWithPath_(html_path)
            url_with_query = NSURL.URLWithString_relativeToURL_(f"?t={int(time.time())}", url)
            self.webview.loadFileURL_allowingReadAccessToURL_(url, url.URLByDeletingLastPathComponent())
            
            # Set Content View Controller
            controller = NSViewController.alloc().init()
            controller.setView_(self.webview)
            self.popover.setContentViewController_(controller)
            self.popover.setContentSize_(self.webview.frame().size)
            
        return self

    def togglePopover_(self, sender):
        debug_print("togglePopover called")
        if self.popover.isShown():
            debug_print("Closing popover")
            self.popover.close()
        else:
            debug_print("Showing popover")
            self.popover.showRelativeToRect_ofView_preferredEdge_(
                sender.bounds(), sender, 1  # NSMinYEdge
            )
            # Trigger update when opened
            self.app.update_price(None, force=False)

    def userContentController_didReceiveScriptMessage_(self, userContentController, message):
        body = message.body()
        action = body.get('action')
        
        if action == 'changeCurrency':
            self.app.change_currency(body.get('currency'))
        elif action == 'updatePrice':
            debug_print("Received updatePrice request from JS")
            self.app.update_price(None, force=True)
        elif action == 'openWebsite':
            webbrowser.open(WEBSITE_URL)
        elif action == 'openAbout':
            icon_path = get_resource_path("bitcoin_tracker_icon.icns")
            rumps.alert(title="BitBar", message="Version 1.0.0\n\nMade with ❤️ by Stoodio™", icon_path=icon_path)
        elif action == 'quitApp':
            rumps.quit_application()
        elif action == 'resizeWindow':
            height = body.get('height')
            if height:
                from Foundation import NSSize
                current_size = self.popover.contentSize()
                new_size = NSSize(current_size.width, height)
                self.popover.setContentSize_(new_size)

class MenuBarApp(rumps.App):
    def __init__(self):
        super(MenuBarApp, self).__init__("BTC", quit_button="Quit")
        self.currency = "usd"
        self.currencies = {
            "usd": "$", "eur": "€", "gbp": "£", "jpy": "¥", 
            "cad": "C$", "aud": "A$", "krw": "₩", "brl": "R$", "try": "₺"
        }
        
        # Set App Icon (Dock and Alerts)
        icon_path = get_resource_path("bitcoin_tracker_icon.icns")
        if os.path.exists(icon_path):
            image = NSImage.alloc().initWithContentsOfFile_(icon_path)
            NSApplication.sharedApplication().setApplicationIconImage_(image)
        
        # Initialize Popover Controller
        self.popover_controller = PopoverController.alloc().initWithApp_(self)
        
        self.last_update_time = 0
        
        # Initial update
        self.update_price(None, force=True)
        
        # Start timer
        self.timer = rumps.Timer(self.update_price, UPDATE_INTERVAL)
        self.timer.start()
        
        # Setup popover after app starts (rumps creates status item in run())
        rumps.Timer(self.setup_popover, 0.1).start()

    def setup_popover(self, sender):
        """Setup popover by attaching it to the status bar button"""
        sender.stop()
        
        try:
            # Access the underlying NSStatusItem via the application delegate
            delegate = NSApplication.sharedApplication().delegate()
            if delegate and hasattr(delegate, 'nsstatusitem'):
                item = delegate.nsstatusitem
                button = item.button()
                
                # Set target and action
                button.setTarget_(self.popover_controller)
                button.setAction_("togglePopover:")
                
                # Remove the menu so the action works
                item.setMenu_(None)
                
                debug_print(f"Popover setup complete - Button: {button}, Target: {button.target()}, Action: {button.action()}")
            else:
                print("Warning: Could not find nsstatusitem in delegate")
        except Exception as e:
            print(f"Error setting up popover: {e}")

    def change_currency(self, currency):
        """Change the display currency"""
        debug_print(f"Changing currency to: {currency}")
        self.currency = currency
        self.update_price(None, force=True)

    def update_price(self, _, force=False):
        """Fetch price data in a background thread"""
        # Check cache if not forced
        if not force and time.time() - self.last_update_time < UPDATE_INTERVAL:
            debug_print("Using cached data")
            return

        t = threading.Thread(target=self._fetch_price, daemon=True)
        t.start()

    def _fetch_price(self):
        """Fetch Bitcoin price data from CoinGecko API"""
        try:
            url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={self.currency}&ids=bitcoin"
            debug_print(f"Fetching: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    self.last_update_time = time.time()
                    self._update_ui(data[0])
                else:
                    print("Error: Empty data received from API")
                    self._send_error_to_ui("No data available")
            elif response.status_code == 429:
                print("Error: API rate limit exceeded (429) - Silently ignoring")
                # Do not update UI, keep old data
            else:
                print(f"Error: API returned {response.status_code}")
                self._send_error_to_ui(f"API Error {response.status_code}")
        except requests.exceptions.Timeout:
            print("Error: Request timeout")
            # self._send_error_to_ui("Request timeout") # Optional: make this silent too if frequent
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            # self._send_error_to_ui("Network error")
        except Exception as e:
            print(f"Unexpected error in _fetch_price: {e}")
            self._send_error_to_ui("Unexpected error")

    def _send_error_to_ui(self, msg):
        """Send error message to UI on main thread"""
        AppHelper.callAfter(self._apply_error_ui, msg)

    def _apply_error_ui(self, msg):
        """Display error in the UI (runs on main thread)"""
        # Use json.dumps to safely escape the message
        js_code = f"showError({json.dumps(msg)})"
        if self.popover_controller and self.popover_controller.webview:
            self.popover_controller.webview.evaluateJavaScript_completionHandler_(js_code, None)

    def _update_ui(self, data):
        """Update UI with new data on main thread"""
        AppHelper.callAfter(self._apply_ui_update, data)

    def _apply_ui_update(self, data):
        """Apply UI updates (runs on main thread)"""
        try:
            from Cocoa import NSAttributedString, NSMutableAttributedString, NSFont, NSColor, NSFontAttributeName, NSForegroundColorAttributeName
            
            current_price = data['current_price']
            symbol = self.currencies.get(self.currency, "$")
            change = data['price_change_percentage_24h']
            
            debug_print(f"Updating UI: {symbol}{current_price} ({change}%)")
            
            # Create attributed string for menu bar
            # Format: ₿ $84,602 ↑0.24%
            
            # Bitcoin symbol: 14px Bold, #EAB308 (yellow)
            bitcoin_text = "₿ "
            bitcoin_attrs = {
                NSFontAttributeName: NSFont.boldSystemFontOfSize_(14),
                NSForegroundColorAttributeName: NSColor.colorWithRed_green_blue_alpha_(0.918, 0.702, 0.031, 1.0)  # #EAB308
            }
            
            # Price: 13px Regular, White
            price_text = f"{symbol}{current_price:,.0f} "
            price_attrs = {
                NSFontAttributeName: NSFont.systemFontOfSize_(13),
                NSForegroundColorAttributeName: NSColor.whiteColor()
            }
            
            # Trend: Arrow (12px) + Percentage (11px)
            # Color: #4ADE80 (up) or #F87171 (down)
            arrow = "↑" if change >= 0 else "↓"
            trend_color = NSColor.colorWithRed_green_blue_alpha_(0.290, 0.871, 0.502, 1.0) if change >= 0 else NSColor.colorWithRed_green_blue_alpha_(0.973, 0.443, 0.443, 1.0)
            
            arrow_text = arrow
            arrow_attrs = {
                NSFontAttributeName: NSFont.systemFontOfSize_(12),
                NSForegroundColorAttributeName: trend_color
            }
            
            percentage_text = f"{abs(change):.2f}%"
            percentage_attrs = {
                NSFontAttributeName: NSFont.systemFontOfSize_(11),
                NSForegroundColorAttributeName: trend_color
            }
            
            # Build attributed string
            attributed_title = NSMutableAttributedString.alloc().init()
            
            bitcoin_part = NSAttributedString.alloc().initWithString_attributes_(bitcoin_text, bitcoin_attrs)
            attributed_title.appendAttributedString_(bitcoin_part)
            
            price_part = NSAttributedString.alloc().initWithString_attributes_(price_text, price_attrs)
            attributed_title.appendAttributedString_(price_part)
            
            arrow_part = NSAttributedString.alloc().initWithString_attributes_(arrow_text, arrow_attrs)
            attributed_title.appendAttributedString_(arrow_part)
            
            percentage_part = NSAttributedString.alloc().initWithString_attributes_(percentage_text, percentage_attrs)
            attributed_title.appendAttributedString_(percentage_part)
            
            # Set attributed title on status bar button
            try:
                delegate = NSApplication.sharedApplication().delegate()
                if delegate and hasattr(delegate, 'nsstatusitem'):
                    button = delegate.nsstatusitem.button()
                    if button:
                        button.setAttributedTitle_(attributed_title)
                else:
                    # Fallback to simple title if we can't access the button
                    self.title = f"₿ {symbol}{current_price:,.0f} {arrow}{abs(change):.2f}%"
            except Exception as e:
                debug_print(f"Could not set attributed title: {e}")
                # Fallback to simple title
                self.title = f"₿ {symbol}{current_price:,.0f} {arrow}{abs(change):.2f}%"
            
            # Update WebView
            json_data = json.dumps(data)
            js_code = f"updateData({json_data})"
            if self.popover_controller and self.popover_controller.webview:
                self.popover_controller.webview.evaluateJavaScript_completionHandler_(js_code, None)
        except KeyError as e:
            print(f"Error: Missing key in data: {e}")
            self._send_error_to_ui("Invalid data format")
        except Exception as e:
            print(f"Error in _apply_ui_update: {e}")
            self._send_error_to_ui("Update failed")

if __name__ == "__main__":
    MenuBarApp().run()
