import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
from datetime import datetime
import threading
import time
import os
from collections import Counter, defaultdict

LOG_FILE = os.path.join(os.path.dirname(__file__), "rugplay_trades.log")
REFRESH_INTERVAL = 5  # seconds

class TradeViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rugplay Trade Viewer")
        self.root.resizable(True, True)

        self.sort_mode = tk.StringVar(value="Newest First")
        self.auto_refresh_enabled = False
        self.stop_refresh = threading.Event()

        self.setup_widgets()

    def setup_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Search Username:").grid(row=0, column=0, sticky="w")
        self.entry = ttk.Entry(frame, width=30)
        self.entry.grid(row=0, column=1, padx=5)

        ttk.Button(frame, text="Search", command=self.search_trades).grid(row=0, column=2)

        self.sort_dropdown = ttk.Combobox(
            frame,
            textvariable=self.sort_mode,
            values=[
                "Newest First", "Oldest First",
                "Most Value", "Least Value",
                "Most Coins", "Least Coins"
            ],
            state="readonly",
            width=15
        )
        self.sort_dropdown.grid(row=0, column=3)
        self.sort_dropdown.bind("<<ComboboxSelected>>", lambda e: self.search_trades())

        self.toggle_button = ttk.Button(frame, text="Auto Refresh: OFF", command=self.toggle_auto_refresh)
        self.toggle_button.grid(row=0, column=4, padx=(10, 0))

        self.info_label = ttk.Label(frame, text="Loading trade summary...", justify="left", padding=(10, 5))
        self.info_label.grid(row=2, column=0, columnspan=5, sticky="w")

        self.text = tk.Text(frame, height=25, width=120)
        self.text.grid(row=3, column=0, columnspan=5, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.text.yview)
        scrollbar.grid(row=3, column=5, sticky="ns")
        self.text.config(yscrollcommand=scrollbar.set)

        self.text.tag_configure("BUY", foreground="green")
        self.text.tag_configure("SELL", foreground="red")

    def load_trades(self, username_filter):
        trades = []
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.search(r'\{.*\}$', line.strip())
                    if not match:
                        continue
                    try:
                        entry = json.loads(match.group())
                        if entry.get("type") == "all-trades":
                            data = entry["data"]
                            username = data.get("username", "").lower()
                            if username_filter in username:
                                trades.append(data)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"'{LOG_FILE}' not found.")
        except Exception as e:
            messagebox.showerror("Read Error", f"An error occurred: {e}")

        sort_by = self.sort_mode.get()
        if sort_by == "Most Value":
            trades.sort(key=lambda x: x.get("totalValue", 0), reverse=True)
        elif sort_by == "Least Value":
            trades.sort(key=lambda x: x.get("totalValue", 0))
        elif sort_by == "Most Coins":
            trades.sort(key=lambda x: x.get("amount", 0), reverse=True)
        elif sort_by == "Least Coins":
            trades.sort(key=lambda x: x.get("amount", 0))
        elif sort_by == "Newest First":
            trades.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        elif sort_by == "Oldest First":
            trades.sort(key=lambda x: x.get("timestamp", 0))
        return trades

    def update_summary_info(self, trades):
        if not trades:
            self.info_label.config(text="No trades to summarize.")
            return

        user_trade_count = Counter()
        user_value_total = defaultdict(float)
        coin_trade_count = Counter()
        coin_user_count = defaultdict(Counter)

        for trade in trades:
            user = trade["username"]
            coin = trade["coinSymbol"]
            value = trade.get("totalValue", 0)

            user_trade_count[user] += 1
            user_value_total[user] += value
            coin_trade_count[coin] += 1
            coin_user_count[coin][user] += 1

        top_trader = user_trade_count.most_common(1)[0][0]
        top_trader_value = max(user_value_total.items(), key=lambda x: x[1])[0]
        top_coin = coin_trade_count.most_common(1)[0][0]
        top_coin_trader = coin_user_count[top_coin].most_common(1)[0][0]

        summary = (
            f"👤 Most Trades: @{top_trader} ({user_trade_count[top_trader]})\n"
            f"💰 Highest Total Value: @{top_trader_value} (${user_value_total[top_trader_value]:,.2f})\n"
            f"🪙 Most Traded Coin: {top_coin} ({coin_trade_count[top_coin]} trades)\n"
            f"🔁 Top {top_coin} Trader: @{top_coin_trader} ({coin_user_count[top_coin][top_coin_trader]} trades)"
        )
        self.info_label.config(text=summary)

    def search_trades(self):
        search_term = self.entry.get().strip().lower()
        self.text.delete("1.0", tk.END)

        trades = self.load_trades(search_term)
        if not trades:
            self.text.insert(tk.END, "No matching trades found.\n")
            self.info_label.config(text="No trades to summarize.")
            return

        for trade in trades:
            formatted = (
                f"{trade['type']:>4} ${trade['totalValue']:,.2f} - "
                f"{trade['amount']:,.2f} {trade['coinSymbol']} by @{trade['username']}\n"
            )
            tag = "BUY" if trade["type"].upper() == "BUY" else "SELL"
            self.text.insert(tk.END, formatted, tag)

        self.update_summary_info(trades)

    def toggle_auto_refresh(self):
        self.auto_refresh_enabled = not self.auto_refresh_enabled
        self.toggle_button.config(text=f"Auto Refresh: {'ON' if self.auto_refresh_enabled else 'OFF'}")

        if self.auto_refresh_enabled:
            self.stop_refresh.clear()
            threading.Thread(target=self.auto_refresh_loop, daemon=True).start()
        else:
            self.stop_refresh.set()

    def auto_refresh_loop(self):
        while not self.stop_refresh.is_set():
            self.search_trades()
            time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeViewerApp(root)
    root.mainloop()
