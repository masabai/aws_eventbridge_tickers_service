GitHub README (The "Why I Built This" Version)
Project: Scheduled Portfolio Tracker (AWS EC2 + Python)
The Problem:
I have a client who needs a daily email update on their $200k portfolio, but they didn't want to pay for a server to run 24/7. They also needed the report to handle tricky data, like when two different stocks have the same ticker symbol (like BBCA).
What I Built:
I set up a "Start-Run-Stop" system on AWS. Instead of the server sitting idle and costing money, it only wakes up for 10 minutes a day to do the work.
How it Works:
The Trigger: AWS EventBridge tells the EC2 instance to "Start" at a specific time.
The Code: As soon as the Linux server boots up, a systemd service kicks off my Python scripts.
The Logic: My script pulls live prices, fixes data errors (like double tickers), and calculates how close the client is to their $200k goal.
The Email: It sends a clean, easy-to-read report using Amazon SES.
The Shutdown: A second EventBridge rule turns the server off so the client only pays for pennies of compute time.
Hard Parts I Solved:
Linux Automation: Getting the script to run immediately on boot using systemd.
Data Cleaning: Writing logic to tell the difference between a Canadian ETF and an Indonesian stock sharing the same ticker.
Permissions: Setting up the IAM Roles so AWS services could talk to each other securely.
Resume Version (No "AI" Buzzwords)
Portfolio Monitoring Service (AWS & Python) | Oct 2025 – Present
Built a live tracking system on AWS EC2 to monitor a $200k+ portfolio, replacing a manual process with an automated daily email report.
Saved 95% on cloud costs by configuring EventBridge to start and stop the instance only during report window hours.
Fixed data accuracy issues by writing Python logic to resolve ticker symbol collisions and correct cost-basis reporting errors.
Automated the Linux environment using systemd to ensure the reporting script executes reliably every time the server boots up.
How to explain the "Daily Bugs" in an interview:
If they ask, "Was it hard to manage?" You say:
"Yeah, it actually taught me a lot about 'dirty' data. For example, I found out the hard way that two different stocks can use the ticker 'BBCA.' I had to update my logic to check the exchange and asset type so the client didn't see a $3,000 error in their report. It's a small script, but the stakes are high because the client sees every mistake."