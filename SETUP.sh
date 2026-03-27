#!/bin/bash
# Bash version of SETUP.bat cho Linux/macOS

set -e

echo "============================================================"
echo "   TY AUTOMATION - SETUP (Linux/macOS)"
echo "============================================================"
echo ""

# 1. Check Python
echo "[1/5] Kiểm tra Python..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "[LỖI] Python chưa cài đặt!"
    echo "Tải Python tại: https://www.python.org/downloads"
    echo ""
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo "   [OK] $PYTHON_VERSION"
echo ""

# 2. Create virtual environment
echo "[2/5] Tạo virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   [OK] Virtual environment tạo thành công"
else
    echo "   [OK] Virtual environment đã tồn tại"
fi
echo ""

# 3. Activate venv and install dependencies
echo "[3/5] Cài đặt Python libraries..."
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "   [OK] Python libraries cài đặt thành công"
echo ""

# 4. Install Playwright browsers
echo "[4/5] Cài đặt Playwright browsers..."
python -m playwright install chromium
python -m playwright install-deps
echo "   [OK] Playwright browsers cài đặt thành công"
echo ""

# 5. Create data directories
echo "[5/5] Tạo thư mục dữ liệu..."
mkdir -p data/profiles
mkdir -p data/logs
mkdir -p data/reports
mkdir -p data/schedules
echo "   [OK] Thư mục tạo thành công"
echo ""

echo "============================================================"
echo "   ✅ SETUP HOÀN THÀNH!"
echo "============================================================"
echo ""
echo "Bước tiếp theo:"
echo "1. Sửa file .env với thông tin Facebook/Notion của bạn"
echo "   cp .env.example .env"
echo "   nano .env"
echo ""
echo "2. Chạy Dashboard:"
echo "   source venv/bin/activate"
echo "   python -m app.dashboard"
echo ""
echo "3. Mở trình duyệt: http://localhost:5000"
echo ""
