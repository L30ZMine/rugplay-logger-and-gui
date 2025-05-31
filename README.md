# 🧾 Rugplay Logger & GUI Viewer

🎮 **Live trade logger** and 🪟 **searchable GUI** for [rugplay.com/live] — track buys/sells with ease!

---

## 🚀 How It Works

- `rugplay-logger.py`: Logs live trades from Rugplay's public WebSocket into `rugplay_trades.log`
- `rugplay_gui.py`: Lets you search, filter, and sort trades from the log file
- Color-coded:
  - 🟩 BUY = green
  - 🟥 SELL = red
- Supports auto-refresh and advanced sorting

---

## 📦 Requirements

Install dependencies first:

```bash
pip install playwright
playwright install
