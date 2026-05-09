# ── Install first (run this in your terminal once): pip install yfinance ──────

# yfinance is a free library that fetches stock data from Yahoo Finance
import yfinance as yf

# datetime lets us get today's date to label our output
import datetime

# ── Define which stocks we want to track ──────────────────────────────────────
# You can change these to any valid ticker symbols
tickers = ["AAPL", "MSFT", "GOOGL", "JPM", "SPY"]

# ── Print a header so the output looks clean ──────────────────────────────────
today = datetime.date.today()
print(f"\n📊 Stock Prices — {today}")
print("-" * 40)

# ── Loop through each ticker and fetch its price ──────────────────────────────
# "for ticker in tickers" means: do this once for each stock in our list
for ticker in tickers:

        # Download the stock's data using yfinance
    stock = yf.Ticker(ticker)

        # .info gives us a dictionary of facts about the stock
        # A dictionary is like a lookup table: key → value
    info = stock.info

        # Pull out the specific numbers we want
        # .get("key", 0) means: get this value, or use 0 if it's missing
    price      = info.get("currentPrice", None)
    prev_close = info.get("previousClose", None)

        # If we couldn't get the price, skip this ticker and warn the user
    if price is None or prev_close is None:
        print(f"{ticker:6}  ⚠️  Could not fetch data")
        continue  # skip to the next ticker

        # Calculate today's change in dollars and percentage
    change_dollar = price - prev_close
    change_pct    = (change_dollar / prev_close) * 100

        # Choose an arrow to show direction at a glance
    arrow = "▲" if change_dollar >= 0 else "▼"

        # Print the result — :.2f means "show 2 decimal places"
        # :+.2f means "always show + or - sign"
    print(f"{ticker:6}  ${price:.2f}   {arrow} {change_dollar:+.2f}  ({change_pct:+.2f}%)")

# ── Footer ────────────────────────────────────────────────────────────────────
print("-" * 40)
print("Data from Yahoo Finance via yfinance\n")