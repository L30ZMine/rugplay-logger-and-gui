#  Rugplay Logger & GUI Viewer

 **Live trade logger** and  **searchable GUI** for [Rugplay Live Trades](rugplay.com/live)

---

##  How It Works

- `rugplay-logger.py`: Logs live trades from Rugplay's public WebSocket into `rugplay_trades.log`
- `rugplay_gui.py`: Lets you search, filter, and sort trades from the log file
- make sure to put both in the same directory
- it runs till infinity (technically 24 days, but this should suffice)

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

![image](https://cdn.discordapp.com/attachments/1378494083730772122/1378494096913727670/64D0A4B0-E8BB-4714-A33F-0771A3F725F4.png)
