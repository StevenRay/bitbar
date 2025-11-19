import rumps
import requests
import webbrowser

class MenuBarApp(rumps.App):

    def __init__(self):
        super(MenuBarApp, self).__init__("BTC Price")
        self.last_price = None
        self.menu = ["Update Price", "Website", "About"]
        
        # Initial update
        self.update_price(None)
        
        # Start timer (15 min interval)
        self.timer = rumps.Timer(self.update_price, 900)
        self.timer.start()

    def update_price(self, _):
        try:
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                current_price = data['bitcoin']['usd']

                percentage_text = ""
                if self.last_price is not None:
                    price_diff = current_price - self.last_price
                    percentage_diff = (price_diff / self.last_price) * 100
                    arrow = "↑" if current_price > self.last_price else "↓"
                    percentage_text = f"{arrow} {abs(percentage_diff):.2f}%"

                self.title = f"₿: ${current_price} {percentage_text}"
                self.last_price = current_price
            else:
                self.title = "BTC: API Error"
        except Exception:
            self.title = "BTC: Offline"

    @rumps.clicked("Update Price")
    def update_price_action(self, _):
        self.update_price(None)

    @rumps.clicked("Website")
    def website(self, _):
        webbrowser.open("http://www.defendersoftheinternet.com")

    @rumps.clicked("About")
    def about(self, _):
        rumps.alert("BitBar made with love by Defenders of the Internet")

if __name__ == "__main__":
    MenuBarApp().run()
