import requests
import boto3
from datetime import datetime

# --- CONFIGURATION
TIINGO_API_KEY = "af8c3a668ae633adda7ace4ad1f74ec6f0bcf3c3"
PORTFOLIO_DATA = {
    # TICKER: (SHARES, TOTAL_ORIGINAL_COST)
    "BBUS":  (1230.62, 151905.94),
    "BBIN":  (412.84,  32411.71),
    "VTIAX": (241.85,  10426.69),
    "BBCA":  (31.47,   3043.20),
    "SHLD":  (6.05,    446.34),
    "GOEX":  (1.88,    174.20)
}

SENDER = "winthutaye@gmail.com"
RECIPIENTS = ["moesabaiaye@yahoo.com"]
AWS_REGION = "us-west-2"

    #url = f"https://api.tiingo.com{ticker}/prices?token={TIINGO_API_KEY}"
    #url = f"https://api.tiingo.com{ticker.lower()}/prices?token={TIINGO_API_KEY}"
    #url = f"https://api.tiingo.com/tiingo/daily/{ticker.lower()}/prices?token={TIINGO_API_KEY}"

def get_tiingo_data(ticker):
    url = f"https://api.tiingo.com{ticker.lower()}/prices?token={TIINGO_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Tiingo returns a LIST, so we take the first item [0]
            data = response.json()[0]
            # Use 'close' as both current and prev to stop the error for now
            return data['close'], data.get('prevClose', data['close'])
    except Exception as e:
        print(f"Connection error for {ticker}: {e}")
    return None, None


def run_portfolio_report():
    now = datetime.now().strftime("%A, %b %d, %Y | %H:%M")
    total_val, total_cost_all, total_day_change = 0, 0, 0
    html_rows = ""

    for ticker, (shares, cost) in PORTFOLIO_DATA.items():
        try:
            price, prev_close = get_tiingo_data(ticker)
            if price:
                current_val = shares * price
                yesterday_val = shares * prev_close
                day_diff = current_val - yesterday_val
                day_pct = ((price - prev_close) / prev_close) * 100
                total_pl = current_val - cost

                total_val += current_val
                total_cost_all += cost
                total_day_change += day_diff

                d_color = "#27ae60" if day_diff >= 0 else "#e74c3c"
                t_color = "#27ae60" if total_pl >= 0 else "#e74c3c"

                # ORDER: TOTAL COST -> SHARES -> PRICE
                html_rows += f"""
                <tr style="font-family: 'Courier New', monospace; border-bottom: 1px solid #eee;">
                    <td style="padding:10px; border:1px solid #ddd;"><b>{ticker}</b></td>
                    <td style="padding:10px; border:1px solid #ddd; background-color:#fcfcfc;">${cost:,.2f}</td>
                    <td style="padding:10px; border:1px solid #ddd;">{shares:,.2f}</td>
                    <td style="padding:10px; border:1px solid #ddd; font-weight:bold;">${price:,.2f}</td>
                    <td style="padding:10px; border:1px solid #ddd; color:{d_color};">{day_diff:+,.2f}</td>
                    <td style="padding:10px; border:1px solid #ddd; color:{d_color};">{day_pct:+.2f}%</td>
                    <td style="padding:10px; border:1px solid #ddd; color:{t_color}; font-weight:bold;">{total_pl:+,.2f}</td>
                    <td style="padding:10px; border:1px solid #ddd; background-color:#f4f7f6;"><b>${current_val:,.2f}</b></td>
                </tr>"""
        except Exception as e:
            print(f"Processing error for {ticker}: {e}")

    net_pl = total_val - total_cost_all
    s_day_color = "#27ae60" if total_day_change >= 0 else "#e74c3c"
    s_tot_color = "#27ae60" if net_pl >= 0 else "#e74c3c"
    progress = (total_val / 200000) * 100

    html_body = f"""
    <html><body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2c3e50;">🔒 PRIVATE ASSET SNAPSHOT</h2>
        <p style="font-size: 0.9em; color: #7f8c8d;">Live Market Update: {now}</p>

        <table style="border-collapse:collapse; width:100%; max-width:1100px; text-align: left;">
            <tr style="background-color:#2c3e50; color: white;">
                <th style="padding:12px;">TICKER</th>
                <th style="padding:12px;">TOTAL COST</th>
                <th style="padding:12px;">SHARES</th>
                <th style="padding:12px;">LIVE PRICE</th>
                <th style="padding:12px;">DAY +/-</th>
                <th style="padding:12px;">DAY %</th>
                <th style="padding:12px;">TOTAL P/L</th>
                <th style="padding:12px;">EST. VALUE</th>
            </tr>
            {html_rows}
        </table>

        <div style="margin-top: 25px; background-color:#f4f7f6; padding:20px; border-radius: 8px; border:1px solid #dcdde1; max-width:1100px;">
            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td><b>NET PORTFOLIO VALUE:</b></td>
                    <td align="right" style="font-size: 1.3em; color:#2c3e50; font-weight:bold;">${total_val:,.2f}</td>
                </tr>
                <tr>
                    <td><b>TODAY PERFORMANCE:</b></td>
                    <td align="right" style="color:{s_day_color}; font-weight:bold;">${total_day_change:+,.2f}</td>
                </tr>
                <tr>
                    <td><b>TOTAL PROFIT/LOSS:</b></td>
                    <td align="right" style="color:{s_tot_color}; font-weight:bold;">${net_pl:+,.2f}</td>
                </tr>
            </table>

            <hr style="border: 0; border-top: 1px solid #dcdde1; margin: 15px 0;">

            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td><b>PROGRESS TO $200K GOAL:</b></td>
                    <td align="right" style="font-weight:bold; color:#2980b9;">{progress:.2f}%</td>
                </tr>
            </table>

            <div style="background-color: #dcdde1; border-radius: 5px; height: 14px; width: 100%; margin-top: 10px;">
                <div style="background-color: #2980b9; height: 14px; width: {min(progress, 100)}%; border-radius: 5px;"></div>
            </div>
        </div>
    </body></html>"""

    ses = boto3.client('ses', region_name=AWS_REGION)
    try:
        ses.send_email(
            Source=SENDER,
            Destination={'ToAddresses': RECIPIENTS},
            Message={
                'Subject': {'Data': f"Tiingo Report: {progress:.2f}% Reached"},
                'Body': {'Html': {'Data': html_body}}
            }
        )
        print("Success! Tiingo-based report sent via SES.")
    except Exception as e:
        print(f"SES Error: {e}")

if __name__ == "__main__":
    run_portfolio_report()
