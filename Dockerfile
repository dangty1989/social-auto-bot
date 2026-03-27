FROM python:3.10-slim

WORKDIR /app

# Cài đặt dependencies hệ thống cho Playwright (browser automation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium-browser \
    chromium-chromedriver \
    ca-certificates \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Cài Python dependencies + Playwright browsers
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m playwright install chromium && \
    python -m playwright install-deps

# Copy toàn bộ app
COPY . .

# Tạo directories cho data
RUN mkdir -p data/profiles data/logs data/reports data/schedules

# Expose ports
# 5000 = Flask Dashboard
# 5678 = n8n (nếu chạy trong Docker)
EXPOSE 5000 5678

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000')" || exit 1

# Run dashboard as default entry point
CMD ["python", "-m", "app.dashboard"]
