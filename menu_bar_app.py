import rumps
import requests
import time
import threading
import webbrowser


class MenuBarApp(rumps.App):

    def __init__(self):
        super(MenuBarApp, self).__init__("BTC Price")
        self.last_price = None
        self.update_price()
        self.menu = ["Update Price", "About"]
        self.start_auto_update()

    def update_price(self):
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        if response.status_code == 200:
            data = response.json()
            current_price = data['bitcoin']['usd']

            if self.last_price is not None:
                price_diff = current_price - self.last_price
                percentage_diff = (price_diff / self.last_price) * 100
                arrow = "↑" if current_price > self.last_price else "↓"
                percentage_text = f"{arrow} {abs(percentage_diff):.2f}%"
            else:
                percentage_text = ""

            self.title = f"₿: ${current_price} {percentage_text}"
            self.last_price = current_price
        else:
            self.title = "BTC Price - Error"

    def start_auto_update(self):
        def update_price_periodically():
            while True:
                self.update_price()
                time.sleep(15 * 60)

        update_thread = threading.Thread(target=update_price_periodically)
        update_thread.daemon = True
        update_thread.start()

    @rumps.clicked("Update Price")
    def update_price_action(self, _):
        self.update_price()

    @rumps.clicked("About")
    def about(self, _):
        rumps.alert("BitBar made with love by Defenders of the Internet")

    @rumps.clicked("Website")
    def website(self, _):
        webbrowser.open("http://www.defendersoftheinternet.com")

if __name__ == "__main__":
    MenuBarApp().run()
