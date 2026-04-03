import asyncio
import requests
from telegram import Bot
from datetime import datetime

# ===== إعدادات =====
TELEGRAM_TOKEN = "8681108447:AAEZspIAsmFTZBITi69B4_y2zKIQoiuMNZQ"
CHAT_ID = "8486432828"
# ====================

bot = Bot(token=TELEGRAM_TOKEN)

def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "1", "interval": "hourly"}
    response = requests.get(url, params=params)
    data = response.json()
    prices = [p[1] for p in data['prices']]
    current_price = prices[-1]
    low_24h = min(prices)
    return current_price, low_24h

async def send_message(text):
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='HTML')

async def monitor_loop():
    alert_sent = False
    while True:
        try:
            current_price, low_24h = get_btc_data()
            diff = ((current_price - low_24h) / low_24h) * 100
            message = (
                f"₿ <b>تحديث البيتكوين</b>\n"
                f"💰 السعر الحالي: <b>${current_price:,.2f}</b>\n"
                f"📉 أدنى سعر (24س): <b>${low_24h:,.2f}</b>\n"
                f"📊 الفرق: <b>{diff:.2f}%</b>\n"
                f"🕐 {datetime.now().strftime('%H:%M:%S')}"
            )
            await send_message(message)
            if diff < 0.5 and not alert_sent:
                await send_message(
                    f"🚨 <b>تنبيه!</b>\nالبيتكوين وصل لأدنى سعر!\n"
                    f"💰 السعر: <b>${current_price:,.2f}</b>\n⚡ فرصة شراء!"
                )
                alert_sent = True
            elif diff >= 1:
                alert_sent = False
        except Exception as e:
            await send_message(f"⚠️ خطأ: {str(e)}")
        await asyncio.sleep(5)

async def main():
    await send_message("🤖 <b>بوت Kemet شغال!</b>\nجاري مراقبة البيتكوين...")
    await monitor_loop()

if __name__ == "__main__":
    asyncio.run(main())
