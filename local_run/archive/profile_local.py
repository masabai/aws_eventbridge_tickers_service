import os
import yfinance as yf
from datetime import datetime

# ANSI Color Codes for a "Pro" look
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# --- PRIVATE PORTFOLIO VALUES
PORTFOLIO_VALUES = {
    "BBUS": 151772.07,
    "BBIN": 32585.46,
    "VTIAX": 10670.45,
    "BBCA": 3029.76,
    "SHLD": 437.16,
    "GOEX": 179.98
}
# BBUS       $   124.71   $126.08          +1.10%     None            (52W High)
def run_value_snapshot():
    # 1. Clear the terminal of those messy file paths
    os.system('cls' if os.name == 'nt' else 'clear')

    now = datetime.now().strftime("%A, %b %d, %Y | %H:%M")
    total_val, total_change = 0, 0

    print(f"\n{BOLD}{'=' * 80}{RESET}")
    print(f"{BOLD}🔒 PRIVATE ASSET SNAPSHOT | {now}{RESET}")
    print(f"{BOLD}{'=' * 80}{RESET}")
    print(f"{'TICKER':<10} {'CURRENT VALUE':<18} {'PRICE':<12} {'DAY %':<12} {'DAY +/-'}")
    print(f"{'-' * 80}")

    for ticker, current_val in PORTFOLIO_VALUES.items():
        try:
            t = yf.Ticker(ticker)
            fast = t.fast_info
            price, prev = fast.last_price, fast.previous_close

            day_pct = ((price - prev) / prev) * 100
            day_cash = current_val * (day_pct / 100)

            total_val += current_val
            total_change += day_cash

            # Pick Color based on performance
            color = GREEN if day_pct >= 0 else RED
            sign = "+" if day_pct >= 0 else ""

            print(f"{BOLD}{ticker:<10}{RESET} "
                  f"${current_val:>13,.2f}   "
                  f"${price:<10.2f} "
                  f"{color}{sign}{day_pct:>8.2f}%{RESET}   "
                  f"{color}{sign}${day_cash:>9,.2f}{RESET}")
        except:
            print(f"Error updating {ticker}")

    # Final Summary
    grand_pct = (total_change / total_val) * 100
    summary_color = GREEN if total_change >= 0 else RED

    print(f"{BOLD}{'=' * 80}{RESET}")
    print(f"{BOLD}{'TOTAL PORTFOLIO VALUE:':<35} ${total_val:>15,.2f}{RESET}")
    print(f"{BOLD}{'TOTAL CHANGE TODAY:':<35} {summary_color}${total_change:>+15,.2f} ({grand_pct:>+5.2f}%){RESET}")
    print(f"{BOLD}{'=' * 80}{RESET}")

    # Progress to $200k Goal
    progress = (total_val / 200000) * 100
    bar = "█" * int(progress / 2) + "░" * (50 - int(progress / 2))
    print(f"\n{BOLD}Progress to $200,000 Goal:{RESET}")
    print(f"|{bar}| {progress:.1f}%")


if __name__ == "__main__":
    run_value_snapshot()
