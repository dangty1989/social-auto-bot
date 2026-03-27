#!/bin/bash
# Chạy Docker Compose cho production (VPS)
# Sử dụng: bash docker-prod.sh

set -e

echo "============================================================"
echo "   TY AUTOMATION - Docker Production Setup"
echo "============================================================"
echo ""

# 1. Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "[CẢNH BÁO] Bạn đang chạy với quyền root!"
    echo "Đó là lý do tại sao Docker hoạt động, nhưng không được khuyến cáo."
    echo ""
fi

# 2. Check Docker
echo "[1/4] Kiểm tra Docker..."
if ! command -v docker &> /dev/null; then
    echo "[LỖI] Docker chưa cài đặt!"
    echo "Tải Docker tại: https://docs.docker.com/engine/install/"
    exit 1
fi
DOCKER_VERSION=$(docker --version)
echo "   [OK] $DOCKER_VERSION"
echo ""

# 3. Check Docker Compose
echo "[2/4] Kiểm tra Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "[LỖI] Docker Compose chưa cài đặt!"
    exit 1
fi
COMPOSE_VERSION=$(docker-compose --version)
echo "   [OK] $COMPOSE_VERSION"
echo ""

# 4. Check .env
echo "[3/4] Kiểm tra file cấu hình..."
if [ ! -f .env ]; then
    echo "[LỖI] File .env không tồn tại!"
    echo "Vui lòng tạo .env từ .env.example và điền thông tin:"
    cp .env.example .env
    echo ""
    echo "Những thông tin REQUIRED cho PRODUCTION:"
    echo "   VPS_DOMAIN=your-domain.com"
    echo "   SSL_EMAIL=your-email@gmail.com"
    echo "   FACEBOOK_EMAIL=your-email@gmail.com"
    echo "   FACEBOOK_PASSWORD=your-password"
    echo "   NOTION_API_KEY=your-notion-key"
    echo ""
    echo "Vui lòng sửa .env và chạy lại script này"
    exit 1
fi

# Check required env variables
REQUIRED_VARS=("VPS_DOMAIN" "SSL_EMAIL" "FACEBOOK_EMAIL" "FACEBOOK_PASSWORD")
for VAR in "${REQUIRED_VARS[@]}"; do
    if ! grep -q "^${VAR}=" .env; then
        echo "[LỖI] Thiếu biến: $VAR trong .env"
        exit 1
    fi
done

echo "   [OK] File .env hợp lệ"
echo ""

# 5. Start Docker Compose Production
echo "[4/4] Khởi động Docker Compose (Production)..."
docker-compose -f docker-compose.prod.yml down || true  # Clean up if running
docker-compose -f docker-compose.prod.yml up -d

echo "   [OK] Containers đang khởi động"
echo ""

# Wait for containers
echo "Đang chờ containers khởi động (60s)..."
sleep 60

# Show status
echo ""
echo "Status containers:"
docker-compose -f docker-compose.prod.yml ps
echo ""

echo "============================================================"
echo "   ✅ DOCKER PRODUCTION SETUP HOÀN THÀNH!"
echo "============================================================"
echo ""

# Get domain from .env
VPS_DOMAIN=$(grep "^VPS_DOMAIN=" .env | cut -d'=' -f2)

echo "Truy cập tại:"
echo "   Dashboard: https://${VPS_DOMAIN}"
echo "   n8n:       https://n8n.${VPS_DOMAIN}"
echo "   Traefik:   http://${VPS_DOMAIN}:8080/dashboard"
echo ""
echo "Lệnh hữu ích:"
echo "   Xem logs:           docker-compose -f docker-compose.prod.yml logs -f"
echo "   Xem status:         docker-compose -f docker-compose.prod.yml ps"
echo "   Restart service:    docker-compose -f docker-compose.prod.yml restart dashboard"
echo "   Dừng tất cả:       docker-compose -f docker-compose.prod.yml down"
echo "   Xem SSL certs:      ls -la ./traefik_data/letsencrypt/"
echo ""
echo "Backup volumes:"
echo "   docker run --rm -v ty-automation-dashboard_profiles:/data -v /backup:/backup alpine tar czf /backup/profiles.tar.gz -C /data ."
echo ""
