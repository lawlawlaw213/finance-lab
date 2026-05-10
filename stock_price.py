# ── Libraries ─────────────────────────────────────────────────────────────────
# Run once in terminal if needed:
# C:/Users/user/AppData/Local/Programs/Python/Python310/python.exe -m pip install yfinance

import yfinance as yf
import datetime
import csv      # built into Python — saves data to spreadsheet-friendly CSV files
import os       # built into Python — helps us work with files and folders

# ── Settings — edit these to customise your tracker ───────────────────────────
TICKERS       = ["AAPL", "MSFT", "GOOGL", "JPM", "SPY"]
ALERT_THRESHOLD = 2.0   # alert if a stock moves more than this % in either direction

# ── Get today's date ──────────────────────────────────────────────────────────
today     = datetime.date.today()
now       = datetime.datetime.now().strftime("%H:%M:%S")  # current time as HH:MM:SS
csv_file  = f"daily_tracker_{today}.csv"                  # e.g. daily_tracker_2026-05-10.csv

# ── Print header ──────────────────────────────────────────────────────────────
print(f"\n{'='*55}")
print(f"  📊 Daily Stock Tracker — {today}  (last run: {now})")
print(f"{'='*55}")
print(f"{'Ticker':<8} {'Price':>9} {'Chg $':>9} {'Chg %':>9}  Status")
print(f"{'-'*55}")

# ── Collect data — we'll store results here for CSV export and summary ────────
results = []   # an empty list we'll fill up as we loop through each ticker
alerts  = []   # a separate list just for stocks that triggered an alert

# ── Loop through each ticker ──────────────────────────────────────────────────
for ticker in TICKERS:
    try:
                # Fetch stock info — wrapped in try/except so one bad ticker won't crash everything
        info       = yf.Ticker(ticker).info
        price      = info.get("currentPrice", None)
        prev_close = info.get("previousClose", None)

        if price is None or prev_close is None:
            print(f"{ticker:<8} {'N/A':>9} {'N/A':>9} {'N/A':>9}  ⚠️  No data")
            continue

                # Calculate change
        chg_dollar = price - prev_close
        chg_pct    = (chg_dollar / prev_close) * 100
        arrow      = "▲" if chg_dollar >= 0 else "▼"

                # Check if this stock crossed the alert threshold
        if abs(chg_pct) >= ALERT_THRESHOLD:   # abs() removes the minus sign so -3% counts too
            status = f"🚨 ALERT {arrow}"
            alerts.append((ticker, chg_pct))  # save for summary section below
        else:
            status = arrow

                # Print the row — :<8 means left-align in 8 chars, :>9 means right-align in 9 chars
        print(f"{ticker:<8} ${price:>8.2f} {chg_dollar:>+9.2f} {chg_pct:>+8.2f}%  {status}")

                # Save this row's data for CSV export later
        results.append({
            "Date"      : str(today),
            "Time"      : now,
            "Ticker"    : ticker,
            "Price"     : round(price, 2),
            "Chg_Dollar": round(chg_dollar, 2),
            "Chg_Pct"   : round(chg_pct, 2),
        })

    except Exception as e:
                # If anything unexpected goes wrong, print a warning and move on
        print(f"{ticker:<8} ⚠️  Error: {e}")

# ── Summary section ───────────────────────────────────────────────────────────
print(f"{'='*55}")

if results:
        # Find best and worst performers using Python's max/min with a sort key
    best  = max(results, key=lambda x: x["Chg_Pct"])
    worst = min(results, key=lambda x: x["Chg_Pct"])
    print(f"  🏆 Best:  {best['Ticker']}  ({best['Chg_Pct']:+.2f}%)")
    print(f"  📉 Worst: {worst['Ticker']} ({worst['Chg_Pct']:+.2f}%)")

if alerts:
    print(f"\n  🚨 Alerts triggered:")
    for t, pct in alerts:
        print(f"     {t} moved {pct:+.2f}% — exceeds {ALERT_THRESHOLD}% threshold")

print(f"{'='*55}\n")

# ── CSV Export ────────────────────────────────────────────────────────────────
# Check if the file already exists so we know whether to write a header row
file_exists = os.path.isfile(csv_file)

with open(csv_file, mode="a", newline="") as f:
        # "a" means append — we add rows without overwriting previous runs today
    fieldnames = ["Date", "Time", "Ticker", "Price", "Chg_Dollar", "Chg_Pct"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()   # only write column names on first run of the day

    writer.writerows(results)  # write all the rows we collected in the loop

print(f"✅ Saved to {csv_file}\n")