#  Rugplay Logger & GUI Viewer

 **Live trade logger** and  **searchable GUI** for [Rugplay Live Trades](rugplay.com/live)

---

##  How It Works

- `rugplay-logger.py`: Logs live trades from Rugplay's public WebSocket into `rugplay_trades.log`
- `rugplay_gui.py`: Lets you search, filter, and sort trades from the log file
- make sure to put both in the same directory

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
