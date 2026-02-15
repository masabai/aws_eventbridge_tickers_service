import os
import yfinance as yf
from datetime import datetime

# ANSI Color Codes
GREEN, RED, YELLOW, BOLD, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[1m", "\033[0m"

# Updated list of 18 Core "Newspaper" Mutual Funds & Tickers
TICKERS = ["BBUS",
    "VFIAX", "VTSAX", "VIGAX", "VSMAX", "VTIAX", "VBTLX",  # Vanguard Core 6
    "FXAIX", "FSKAX", "FZROX", "FNILX", "FBGRX", "FDGRX",  # Fidelity Core 6
    "SWPPX", "SWTSX", "SWLGX", "SFLNX", "DODGX", "PREIX"   # Schwab & Industry Core 6
]

def run_prediction_report():
    os.system('cls' if os.name == 'nt' else 'clear')
    now = datetime.now().strftime("%A, %b %d, %Y | %H:%M")

    print(f"\n{BOLD}{'=' * 95}{RESET}")
    print(f"{BOLD}📊 FUND PERFORMANCE & TARGET SNAPSHOT | {now}{RESET}")
    print(f"{BOLD}{'=' * 95}{RESET}")
    print(f"{'TICKER':<10} {'PRICE':<12} {'1Y TARGET':<15} {'UPSIDE %':<12} {'FUND RATING'}")
    print(f"{'-' * 95}")

    for ticker in TICKERS:
        try:
            t = yf.Ticker(ticker)
            info = t.info

            current = info.get('regularMarketPrice') or info.get('navPrice') or info.get('previousClose') or 0.0

            # Use Analyst Target; fallback to 52-Week High if N/A
            target = info.get('targetMeanPrice')
            target_source = "Analyst"
            if not target:
                target = info.get('fiftyTwoWeekHigh')
                target_source = "52W High"

            rating = info.get('recommendationKey') or info.get('trailingAnnualDividendYield')
            if isinstance(rating, float):
                rating = f"Yield: {rating * 100:.2f}%"
            else:
                rating = str(rating).replace('_', ' ').title()

            upside_str, color = "N/A", RESET
            if target and current:
                upside = ((target - current) / current) * 100
                color = GREEN if upside > 0 else RED
                upside_str = f"{upside:>+7.2f}%"

            r_color = YELLOW
            if "Buy" in rating or "Strong" in rating:
                r_color = GREEN
            elif "Sell" in rating:
                r_color = RED

            print(f"{BOLD}{ticker:<10}{RESET} "
                  f"${current:>9.2f}   "
                  f"${str(f'{target:.2f}') if target else 'N/A':<13} "
                  f"{color}{upside_str:<12}{RESET} "
                  f"{r_color}{rating:<15}{RESET} ({target_source})")
        except Exception:
            print(f"Error updating {ticker}")

    # EXPLANATION NOTE
    print(f"{'-' * 95}")
    print(f"{BOLD}NOTE ON PREDICTIONS:{RESET}")
    print(
        f"• {BOLD}1Y TARGET:{RESET} Professional analyst estimate for 12 months. (Uses {BOLD}52W High{RESET} as a proxy for funds).")
    print(
        f"• {BOLD}UPSIDE %:{RESET} Predicted gain to reach target. {GREEN}Green{RESET} is undervalued; {RED}Red{RESET} is near peak.")
    print(f"• {BOLD}2026 BENCHMARK:{RESET} Major banks (Morgan Stanley/Deutsche Bank) forecast S&P 500 targets")
    print(f"  between {BOLD}7,800 and 8,000{RESET}, implying a broad market upside of ~12-16% for this year.")
    print(f"{BOLD}{'=' * 95}{RESET}\n")


if __name__ == "__main__":
    run_prediction_report()
