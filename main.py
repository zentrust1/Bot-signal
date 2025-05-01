import os
import requests
import pandas as pd

API_KEY = os.getenv("TWELVE_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

symbol = "XAU/USD"
interval = "5min"

url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize=5&apikey={API_KEY}"
response = requests.get(url).json()

if "values" not in response:
    print("Gagal ambil data:", response)
    exit()

df = pd.DataFrame(response["values"])
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.astype({"open": float, "high": float, "low": float, "close": float})
df = df.sort_values("datetime")

latest = df.iloc[-1]
previous = df.iloc[-2]
entry = latest["close"]

# Aturan TP dan SL (dalam pips = 0.10 untuk XAU/USD)
TP_PIPS = 1.0  # = 100 pips
SL_PIPS = 0.5  # = 50 pips

signal = ""
tp = 0
sl = 0

if entry > previous["high"]:
    signal = "BUY"
    tp = round(entry + TP_PIPS, 2)
    sl = round(entry - SL_PIPS, 2)
elif entry < previous["low"]:
    signal = "SELL"
    tp = round(entry - TP_PIPS, 2)
    sl = round(entry + SL_PIPS, 2)
else:
    signal = None

# Kirim sinyal ke Telegram
if signal:
    message = f"""{signal} XAU/USD
Entry: {entry}
TP: {tp}
SL: {sl}
Time: {latest['datetime']}"""
else:
    message = f"Tidak ada sinyal.\nHarga: {entry}"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": message
}
r = requests.post(telegram_url, data=payload)
print("Pesan terkirim:", r.status_code)
