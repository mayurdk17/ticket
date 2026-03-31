import asyncio
import requests
import os
from playwright.async_api import async_playwright

# 🔐 ENV VARIABLES (from Render)
TELEGRAM_TOKEN = os.getenv("8376263102:AAGrJBhDW3mPjb0b2_tekQ1grG3huI24EXc")
CHAT_ID = os.getenv("5526791148)

URL = "https://shop.royalchallengers.com/ticket"

def send_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
    except Exception as e:
        print("Telegram error:", e)

async def run():
    print("🚀 Bot started...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,  # ✅ REQUIRED for cloud
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(URL)

        while True:
            try:
                print("🔄 Checking page...")

                # 🔍 Look for Buy button or ticket availability
                content = await page.content()

                if "Buy Tickets" in content or "Book Now" in content:
                    print("🔥 TICKETS FOUND!")
                    send_telegram("🔥 RCB Tickets LIVE! Go book NOW!")

                    # Try clicking automatically
                    try:
                        await page.click("text=Buy")
                        print("✅ Clicked Buy button")
                    except:
                        pass

                    await asyncio.sleep(10)  # prevent spam

                else:
                    print("❌ Not available yet")

                await asyncio.sleep(2)  # ⚡ FAST polling

                await page.reload()

            except Exception as e:
                print("Error:", e)
                await asyncio.sleep(5)

asyncio.run(run())
