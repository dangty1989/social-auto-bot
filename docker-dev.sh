#!/bin/bash
# Chạy Docker Compose cho development
# Sử dụng: bash docker-dev.sh

set -e

echo "============================================================"
echo "   TY AUTOMATION - Docker Development Setup"
echo "============================================================"
echo ""

# 1. Check Docker
echo "[1/4] Kiểm tra Docker..."
if ! command -v docker &> /dev/null; then
    echo "[LỖI] Docker chưa cài đặt!"
    echo "Tải Docker tại: https://www.docker.com/products/docker-desktop"
    exit 1
fi
DOCKER_VERSION=$(docker --version)
echo "   [OK] $DOCKER_VERSION"
echo ""

# 2. Check Docker Compose
echo "[2/4] Kiểm tra Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "[LỖI] Docker Compose chưa cài đặt!"
    exit 1
fi
COMPOSE_VERSION=$(docker-compose --version)
echo "   [OK] $COMPOSE_VERSION"
echo ""

# 3. Copy .env if not exists
echo "[3/4] Chuẩn bị file cấu hình..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   [!] File .env đã được tạo từ .env.example"
    echo "   [!] Vui lòng chỉnh sửa .env với thông tin của bạn"
    echo ""
    echo "Những thông tin cần thêm vào .env:"
    echo "   FACEBOOK_EMAIL=your-email@gmail.com"
    echo "   FACEBOOK_PASSWORD=your-password"
    echo "   NOTION_API_KEY=your-notion-key"
    echo ""
    read -p "Nhấn Enter khi đã sửa .env..."
else
    echo "   [OK] File .env đã tồn tại"
fi
echo ""

# 4. Start Docker Compose
echo "[4/4] Khởi động Docker Compose..."
docker-compose up -d
echo "   [OK] Containers đang khởi động"
echo ""

# Wait for containers to be healthy
echo "Đang chờ containers khởi động (30s)..."
sleep 30

echo ""
echo "============================================================"
echo "   ✅ DOCKER SETUP HOÀN THÀNH!"
echo "============================================================"
echo ""
echo "Truy cập:"
echo "   Dashboard: http://localhost:5000"
echo "   n8n (nếu enable): http://localhost:5678"
echo ""
echo "Lệnh hữu ích:"
echo "   Xem logs:       docker-compose logs -f"
echo "   Dừng services: docker-compose down"
echo "   Restart:       docker-compose restart dashboard"
echo ""
