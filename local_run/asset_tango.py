import json
import urllib.request
import os
from datetime import datetime

# --- CONFIGURATION
# 1. Double check your token at https://api.tiingo.com
TIINGO_API_KEY =  "af8c3a668ae633adda7ace4ad1f74ec6f0bcf3c3"

PORTFOLIO_DATA = {
    "BBUS": (151772.07, 154206.07),
    "BBIN": (32585.46, 33609.00),
    "VTIAX": (10670.45, 10532.05),
    "BBCA": (3029.76, 3111.44),
    "SHLD": (437.16, 450.12),
    "GOEX": (179.98, 190.99),
}


def get_tiingo_data(ticker):
    # This 'iex' endpoint is better for 'Last Price' + 'Prev Close' in one call
    url = f"https://api.tiingo.com{ticker}&token={TIINGO_API_KEY}"

    try:
        # 10 second timeout to prevent freezing
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            # IEX returns a LIST of dicts: [{'ticker': 'BBUS', 'last': 123, ...}]
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            return None
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None


def run_snapshot():
    now = datetime.now().strftime("%A, %b %d, %Y | %H:%M")
    total_val_now, total_cost, total_day_change = 0, 0, 0

    print(f"\n{'=' * 95}\n🔒 PRIVATE ASSET SNAPSHOT | {now}\n{'=' * 95}")
    print(f"{'TICKER':<10} {'CURRENT VAL':<15} {'DAY +/-':<12} {'DAY %':<10} {'TOTAL P/L':<12} {'PRICE'}")
    print('-' * 95)

    for ticker, (prev_total_val, cost_basis) in PORTFOLIO_DATA.items():
        data = get_tiingo_data(ticker)

        if not data:
            continue

        # Tiingo IEX fields: 'last' (current) and 'prevClose'
        current_price = data.get('last')
        prev_close = data.get('prevClose')

        if current_price and prev_close:
            day_pct = (current_price - prev_close) / prev_close
            current_total_val = prev_total_val * (1 + day_pct)
            day_cash_diff = current_total_val - prev_total_val
            total_pl_cash = current_total_val - cost_basis

            total_val_now += current_total_val
            total_cost += cost_basis
            total_day_change += day_cash_diff

            print(f"{ticker:<10} "
                  f"${current_total_val:>11,.2f}  "
                  f"${day_cash_diff:>10,.2f}   "
                  f"{day_pct * 100:>+7.2f}%    "
                  f"{total_pl_cash:>11,.2f}    "
                  f"${current_price:<8.2f}")

    # Summary
    total_pl_all = total_val_now - total_cost
    print(f"{'=' * 95}\n{'NET PORTFOLIO VALUE:':<35} ${total_val_now:>15,.2f}")
    print(f"{'TODAY PERFORMANCE:':<35} ${total_day_change:>+15,.2f}")
    print(f"{'TOTAL PROFIT/LOSS:':<35} ${total_pl_all:>+15,.2f}\n{'=' * 95}")

    # Progress Bar
    progress = min((total_val_now / 200000) * 100, 100)
    bar = "█" * int(progress / 2) + "░" * (50 - int(progress / 2))
    print(f"\nProgress to $200,000 Goal: {progress:.1f}%\n|{bar}|")


if __name__ == "__main__":
    run_snapshot()
