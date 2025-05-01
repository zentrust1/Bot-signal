import os
import requests
import pandas as pd

# Load environment variables
API_KEY = os.getenv("TWELVE_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
symbol = "XAU/USD"
interval = "5min"

# Fetch price data
url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize=5&apikey={API_KEY}"
response = requests.get(url).json()

if "values" not in response:
    print("Failed to fetch data:", response)
    exit()

df = pd.DataFrame(response["values"])
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.astype({"open": float, "high": float, "low": float, "close": float})
df = df.sort_values("datetime")

latest = df.iloc[-1]
previous = df.iloc[-2]

# Simple breakout detection
if latest["close"] > previous["high"]:
    message = f"📈 Breakout NAIK XAU/USD!\nHarga: {latest['close']}\nWaktu: {latest['datetime']}"
elif latest["close"] < previous["low"]:
    message = f"📉 Breakout TURUN XAU/USD!\nHarga: {latest['close']}\nWaktu: {latest['datetime']}"
else:
    message = f"ℹ️ Tidak ada breakout.\nHarga terakhir: {latest['close']}"

# Send to Telegram
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": message
}
r = requests.post(telegram_url, data=payload)
print("Pesan terkirim:", r.status_code)
