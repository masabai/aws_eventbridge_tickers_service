"""
Portfolio Reporting Service
---------------------------
Generates a daily portfolio valuation report and emails results via Amazon SES.

This script is designed to run automatically on EC2 via systemd and
scheduled start/stop using AWS EventBridge.

NOTE:
Portfolio holdings, values, and email recipients are DEMONSTRATION DATA ONLY.
This project showcases automation, reporting, and AWS service integration.
"""

import yfinance as yf
import boto3
from datetime import datetime

# --- CONFIGURATION
# Verified Data for Friday, Feb 13, 2026
PORTFOLIO_DATA = {
    # TICKER: (SHARES, TOTAL_ORIGINAL_COST)
    "BBUS": (1230.62, 151905.94),
    "BBIN": (412.84, 32411.71),
    "VTIAX": (241.85, 10426.69),
    "BBCA": (31.47, 3043.20),
    "SHLD": (6.05, 446.34),
    "GOEX": (1.88, 174.20)
}

SENDER = "abc@example.com"
RECIPIENTS =["airflow@abc.com"]
AWS_REGION = "us-west-2"


def run_portfolio_report():
    now = datetime.now().strftime("%A, %b %d, %Y | %H:%M")
    total_val, total_cost_all, total_day_change = 0, 0, 0
    html_rows = ""

    for ticker, (shares, cost) in PORTFOLIO_DATA.items():
        try:
            t = yf.Ticker(ticker)
            fast = t.fast_info
            price = fast.last_price
            prev_close = fast.previous_close

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

            # UPDATED ORDER: TOTAL COST -> SHARES -> PRICE
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
            print(f"Error fetching {ticker}: {e}")

    net_pl = total_val - total_cost_all
    s_day_color = "#27ae60" if total_day_change >= 0 else "#e74c3c"
    s_tot_color = "#27ae60" if net_pl >= 0 else "#e74c3c"
    progress = (total_val / 200000) * 100

    html_body = f"""
    <html><body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2c3e50;"> PRIVATE ASSET SNAPSHOT</h2>
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

            <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                <b>  NET PORTFOLIO VALUE:</b>
                <span style="font-size: 1.3em; color:#2c3e50; font-weight:bold;">${total_val:,.2f}</span>
            </div>

            <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                <b>  TODAY PERFORMANCE:</b>
                <span style="color:{s_day_color}; font-weight:bold;">${total_day_change:+,.2f}</span>
            </div>

            <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                <b>  TOTAL PROFIT/LOSS:</b>
                <span style="color:{s_tot_color}; font-weight:bold;">${net_pl:+,.2f}</span>
            </div>

            <hr style="border: 0; border-top: 1px solid #dcdde1; margin: 15px 0;">

            <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                <b>PROGRESS TO $200K GOAL:</b>
                <span style="font-weight:bold; color:#2980b9;">{progress:.2f}%</span>
            </div>

            <div style="background-color: #dcdde1; border-radius: 5px; height: 14px; width: 100%; margin-top: 10px;">
                <div style="background-color: #2980b9; height: 14px; width: {min(progress, 100)}%; border-radius: 5px;"></div>
            </div>
        </div>
    </body></html>""" # End of html_body

    ses = boto3.client('ses', region_name=AWS_REGION)
    try:
        ses.send_email(
            Source=SENDER,
            Destination={'ToAddresses': RECIPIENTS},
            Message={
                'Subject': {'Data': f"Asset Report: {progress:.2f}% of Goal Reached"},
                'Body': {'Html': {'Data': html_body}}
            }
        )
        print(f"Report sent successfully. Order: Cost, Shares, Price.")
    except Exception as e:
        print(f"SES Error: {e}")


if __name__ == "__main__":
    run_portfolio_report()
