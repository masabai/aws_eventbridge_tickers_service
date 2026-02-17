# 1. Use slim Python (less RAM and Disk space)
FROM python:3.11-slim

# 2. Set the "home" folder inside the container
WORKDIR /app

# 3. Copy local files (script + requirements) into the container
COPY . .

# 4. Install libraries so the container has them
RUN pip install --no-cache-dir yfinance boto3

# 5. Run the scripts"
CMD ["sh", "-c", "python mfunds_ses_k8.py && python asset_k8.py"]

