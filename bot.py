import asyncio
from playwright.async_api import async_playwright
import requests

URL = "https://shop.royalchallengers.com/ticket"

TELEGRAM_TOKEN = "P8364806766:AAGZZNu-EcFGsfiXHdAtruyTm8IXyGjv7-g"
CHAT_ID = "PAS5526791148"

A_KEYWORDS = ["A Stand", "A-Stand", "Stand A"]

def send_alert(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
    except:
        print("Telegram error")

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # visible for testing
        context = await browser.new_context()
        page = await context.new_page()

        # Speed boost (optional)
        await page.route("**/*", lambda route:
            route.abort() if route.request.resource_type in ["image", "font"] else route.continue_()
        )

        await page.goto(URL)

        print("Bot started...")

        while True:
            try:
                # 🔥 TEST: Trigger BUY alert if button exists (even if disabled)
                buy = await page.query_selector("text=Buy")
                if buy:
                    print("TEST: Buy button detected")
                    send_alert("🚨 TEST: BUY BUTTON DETECTED!")
                    await asyncio.sleep(5)  # avoid spam

                # 🔥 TEST: Detect ANY Stand (simulate A Stand detection)
                stands = await page.query_selector_all("text=Stand")

                for s in stands:
                    text = await s.inner_text()
                    print("Found stand:", text)

                    if any(k in text for k in A_KEYWORDS):
                        print("TEST: A STAND FOUND")
                        send_alert("🔥 TEST: A STAND DETECTED!")
                        await asyncio.sleep(5)

                print("Checking again...")
                await asyncio.sleep(2)
                await page.reload()

            except Exception as e:
                print("Error:", e)
                await page.reload()

asyncio.run(run())