
import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from time import sleep

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

URL = "https://kolesa.kz/cars/renault/duster/astana/?year[from]=2013&year[to]=2015&price[to]=4500000&run[to]=300000"

sent_links = set()

def get_listings():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select(".a-list .a-card")

    listings = []
    for item in items:
        title = item.select_one(".a-card__title").get_text(strip=True)
        price = item.select_one(".a-card__price").get_text(strip=True)
        link = "https://kolesa.kz" + item.select_one("a")["href"]
        image = item.select_one("img")["src"]
        listings.append({"title": title, "price": price, "link": link, "image": image})
    return listings

def notify_new_listings():
    global sent_links
    listings = get_listings()
    for item in listings:
        if item["link"] not in sent_links:
            msg = f"{item['title']}
{item['price']}
{item['link']}"
            try:
                bot.send_photo(chat_id=CHAT_ID, photo=item["image"], caption=msg)
            except Exception as e:
                print("Failed to send:", e)
            sent_links.add(item["link"])

if __name__ == "__main__":
    while True:
        notify_new_listings()
        sleep(600)  # Проверять каждые 10 минут
