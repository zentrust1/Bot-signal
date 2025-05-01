# XAU/USD Breakout Signal Bot

Bot ini mendeteksi breakout pada pair XAU/USD setiap 5 menit menggunakan data dari Twelve Data dan mengirimkan notifikasi ke Telegram.

## Fitur

- Deteksi breakout naik dan turun.
- Notifikasi otomatis ke Telegram.
- Dijadwalkan setiap 5 menit menggunakan GitHub Actions.

## Penggunaan

1. Fork repositori ini.
2. Tambahkan secrets berikut di `Settings > Secrets and variables > Actions`:
   - `TWELVE_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. Workflow akan berjalan otomatis setiap 5 menit.
