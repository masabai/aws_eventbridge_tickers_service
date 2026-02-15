import os
import yfinance as yf
from datetime import datetime

GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# --- UPDATED DATA STRUCTURE
# FORMAT: "TICKER": (Total Current Value, Total Original Cost)
# --- ADJUSTED DATA (Cost Basis tuned to match your requested P/L)
PORTFOLIO_DATA = {
    # Current Val - Gain = Adjusted Cost Basis
    "BBUS": (151772.07, 151905.94),  # Loss: -133.87
    "BBIN": (32585.46, 32411.71),  # Gain: +173.75
    "VTIAX": (10670.45, 10426.69),  # Total Gain: +243.76 (165.30 + 78.46)
    "BBCA": (3029.76, 3043.20),  # Loss: -13.44
    "SHLD": (437.16, 446.34) , # Loss: -9.18
    "GOEX": (179.98, 174.20),  # Gain: +5.78
}


def run_value_snapshot():
    os.system('cls' if os.name == 'nt' else 'clear')
    now = datetime.now().strftime("%A, %b %d, %Y | %H:%M")

    total_val, total_cost, total_day_change = 0, 0, 0

    print(f"\n{BOLD}{'=' * 95}{RESET}")
    print(f"{BOLD}🔒 PRIVATE ASSET SNAPSHOT | {now}{RESET}")
    print(f"{BOLD}{'=' * 95}{RESET}")
    print(f"{'TICKER':<10} {'CURRENT VAL':<15} {'DAY +/-':<12} {'DAY %':<10} {'TOTAL P/L':<12} {'PRICE'}")
    print(f"{'-' * 95}")

    for ticker, (current_val, cost_basis) in PORTFOLIO_DATA.items():
        try:
            t = yf.Ticker(ticker)
            # Use basic info for faster execution
            info = t.fast_info
            price = info.last_price
            prev_close = info.previous_close

            # 1. Day Performance (Today's move)
            day_pct = ((price - prev_close) / prev_close)

            # Treat stored current_val as yesterday close value
            base_val = current_val

            # Calculate today's updated value
            today_val = base_val * (1 + day_pct)

            # Dollar change for today
            day_cash_diff = today_val - base_val

            # 2. Total Performance (Since Purchase)
            total_pl_cash = today_val - cost_basis
            total_pl_pct = (total_pl_cash / cost_basis) * 100

            # Update totals using today_val (NOT current_val)
            total_val += today_val
            total_cost += cost_basis
            total_day_change += day_cash_diff

            # Colors
            day_color = GREEN if day_cash_diff >= 0 else RED
            total_color = GREEN if total_pl_cash >= 0 else RED

            print(f"{BOLD}{ticker:<10}{RESET} "
                  f"${current_val:>11,.2f}  "
                  f"${price:<8.2f}"
                  f"{day_color}{day_cash_diff:>+10,.2f}{RESET} "
                  f"{day_color}{day_pct * 100:>+8.2f}%{RESET}  "
                  f"{total_color}{total_pl_cash:>+11,.2f}{RESET}"
                  )
                  #f"${price:<8.2f}")
        except Exception as e:
            print(f"Error updating {ticker}: {e}")

    # Final Summary Logic
    total_pl_all = total_val - total_cost
    summary_day_color = GREEN if total_day_change >= 0 else RED
    summary_total_color = GREEN if total_pl_all >= 0 else RED

    print(f"{BOLD}{'=' * 95}{RESET}")
    print(f"{BOLD}{'NET PORTFOLIO VALUE:':<35} ${total_val:>15,.2f}{RESET}")
    print(f"{'TODAY PERFORMANCE:':<35} {summary_day_color}${total_day_change:>+15,.2f}{RESET}")
    print(f"{'TOTAL PROFIT/LOSS:':<35} {summary_total_color}${total_pl_all:>+15,.2f}{RESET}")
    print(f"{BOLD}{'=' * 95}{RESET}")

    # Progress Bar
    progress = (total_val / 200000) * 100
    bar = "█" * int(progress / 2) + "░" * (50 - int(progress / 2))
    print(f"\n{BOLD}Progress to $200,000 Goal: {progress:.1f}%{RESET}")
    print(f"|{bar}|")


if __name__ == "__main__":
    run_value_snapshot()
