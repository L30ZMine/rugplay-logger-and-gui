from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "rugplay_trades.log")

def try_log(payload):
    try:
        data = json.loads(payload)
        if isinstance(data, dict) and data.get("type") == "all-trades":
            log_entry = f"[{datetime.now()}] {json.dumps(data)}\n"
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
                f.flush()
            print("📝 Logged:", log_entry.strip())
    except Exception as e:
        print(f"[⚠️ Error] Could not parse/write: {e}")

def log_trades():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def handle_ws(ws):
            ws.on("framereceived", lambda frame: try_log(frame))

        page.on("websocket", handle_ws)
        page.goto("https://rugplay.com/live")

        print("🔁 Logging live trades... Press Ctrl+C to stop.")
        while True:
            page.wait_for_timeout(2_000_000_000)  # Just under 24 days (becuase of 24signed integer and im too lazy to change it looolzzz)

if __name__ == "__main__":
    log_trades()
