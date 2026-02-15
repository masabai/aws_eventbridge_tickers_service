import boto3
import yfinance as yf
from botocore.exceptions import ClientError
from datetime import datetime

# --- CONFIGURATION ---
RECIPIENTS =["airflow@example.com", "user@comcast.net"]
AWS_REGION = "us-west-2"
AWS_REGION = "us-west-2"

# The 18 "Newspaper" Core Mutual Funds
TICKERS = [
    "VFIAX", "VTSAX", "VIGAX", "VSMAX", "VTIAX", "VBTLX",
    "FXAIX", "FSKAX", "FZROX", "FNILX", "FBGRX", "FDGRX",
    "SWPPX", "SWTSX", "SWLGX", "SFLNX", "DODGX", "PREIX"
]

def generate_html_table():
    rows = ""
    for ticker in TICKERS:
        try:
            t = yf.Ticker(ticker)
            info = t.info
            price = info.get('regularMarketPrice') or info.get('navPrice') or info.get('previousClose') or 0.0
            target = info.get('targetMeanPrice') or info.get('fiftyTwoWeekHigh') or 0.0
            upside = ((target - price) / price) * 100 if target > 0 and price > 0 else 0.0
            color = "#28a745" if upside > 0 else "#dc3545"
            rows += f"""
            <tr>
                <td style="padding:12px; border-bottom:1px solid #eee;"><b>{ticker}</b></td>
                <td style="padding:12px; border-bottom:1px solid #eee;">${price:,.2f}</td>
                <td style="padding:12px; border-bottom:1px solid #eee; color:{color}; font-weight:bold;">{upside:+.2f}%</td>
            </tr>
            """
        except:
            continue
    return rows

def send_ses_report():
    ses = boto3.client('ses', region_name=AWS_REGION)
    now = datetime.now().strftime("%B %d, %Y")

    # Summary notes moved into the email HTML
    summary_notes = f"""
    <div style="margin-top:20px; padding:15px; background-color:#f0f8ff; border-left:4px solid #004a99; font-size:13px; color:#333;">
        <b>NOTE ON PREDICTIONS:</b><br>
        • 1Y TARGET: Professional analyst estimate for 12 months. (Uses 52W High as a proxy for funds).<br>
        • UPSIDE %: Predicted gain to reach target. Green is undervalued; Red is near peak.<br>
        • 2026 BENCHMARK: Major banks (Morgan Stanley/Deutsche Bank) forecast S&P 500 targets between 7,800 and 8,000, implying a broad market upside of ~12-16% for this year.
    </div>
    """

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="max-width:600px; margin:auto; border:1px solid #eee; padding:20px; border-radius:8px;">
            <h2 style="color:#004a99; border-bottom:2px solid #004a99; padding-bottom:10px;">Market Snapshot: {now}</h2>
            <p>Daily prediction report for core mutual fund holdings:</p>
            <table style="width:100%; border-collapse:collapse;">
                <thead style="background-color:#f4f4f4;">
                    <tr>
                        <th style="text-align:left; padding:12px;">Ticker</th>
                        <th style="text-align:left; padding:12px;">Price</th>
                        <th style="text-align:left; padding:12px;">Predicted Upside</th>
                    </tr>
                </thead>
                <tbody>
                    {generate_html_table()}
                </tbody>
            </table>
            <div style="margin-top: 20px; padding: 15px; background-color: #f9f9f9; font-size: 11px; color: #777;">
                Note: Predictions based on analyst targets or 52W peaks via <a href="https://finance.yahoo.com">Yahoo Finance</a>.
            </div>

            {summary_notes}  <!-- Added summary into email -->
        </div>
    </body>
    </html>
    """

    try:
        response = ses.send_email(
            Source=SENDER,
            Destination={'ToAddresses': RECIPIENTS},
            Message={
                'Subject': {'Data': f"Daily Prediction Report - {now}", 'Charset': 'UTF-8'},
                'Body': {'Html': {'Data': html_body, 'Charset': 'UTF-8'}}
            }
        )
        print(f"Success! Email sent to {RECIPIENTS}. ID: {response['MessageId']}")
    except ClientError as e:
        print(f"SES Error: {e.response['Error']['Message']}")

if __name__ == "__main__":
    send_ses_report()
