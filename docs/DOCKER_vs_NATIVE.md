# 🐳 Hướng Dẫn: Setup Native vs Docker

**Repo này hỗ trợ cả 2 cách chạy:**
1. **Native (Hiện tại)** → Chạy trực tiếp trên máy Windows/Linux (không cần Docker)
2. **Docker** → Chạy trong container (Docker Desktop hoặc VPS)

---

## 📊 So Sánh

| Tiêu Chí | Native | Docker |
|----------|--------|--------|
| **Cài đặt** | 2-3 phút | 5-10 phút |
| **Yêu cầu** | Python 3.10+ | Docker Desktop/Server |
| **Phù hợp với** | Máy cá nhân, Windows | VPS, Linux, Production |
| **Quản lý** | Thủ công | Tự động (env vars) |
| **Backup** | Thủ công (data/) | Volume Docker |
| **Mở rộng** | Khó | Dễ (scale containers) |
| **SSL/HTTPS** | Không | Có (Traefik) |

---

## 🚀 CÁCH 1: Native Setup (Máy Không Docker)

### **Yêu Cầu**
- Windows 10+ hoặc macOS/Linux
- Python 3.10+ (link: https://www.python.org/downloads)
- 2GB RAM, 500MB disk space

### **Bước 1: Download & Setup**
```bash
# 1. Clone repo
git clone <repo-url> social-auto-bot
cd social-auto-bot

# 2. Chạy SETUP.bat (Windows) hoặc SETUP.sh (Linux/Mac)
# Windows:
SETUP.bat

# Linux/Mac:
bash -c "python -m pip install -r requirements.txt && python -m playwright install"
```

### **Bước 2: Cấu Hình**
```bash
# 1. Copy mẫu config
cp .env.example .env

# 2. Mở .env, thêm thông tin:
FACEBOOK_EMAIL=your-email@gmail.com
FACEBOOK_PASSWORD=your-password
NOTION_API_KEY=your-notion-key
```

### **Bước 3: Chạy Dashboard**
```bash
# Windows: Nhấp đúp DASHBOARD.bat
# Linux/Mac:
python -m app.dashboard
# Mở: http://localhost:5000
```

### **Ưu Điểm**
✅ Cài đặt nhanh  
✅ Không phức tạp  
✅ Dễ debug  
✅ Tiêu thụ ít tài nguyên  

### **Nhược Điểm**
❌ Chỉ chạy trên máy này  
❌ Khó backup/migrate  
❌ Không có SSL  
❌ Khó deploy lên VPS  

---

## 🐳 CÁCH 2: Docker Setup (VPS hoặc Docker Desktop)

### **Yêu Cầu**
- **Docker Desktop** (Windows/Mac): https://www.docker.com/products/docker-desktop
- **Docker Server** (VPS): https://docs.docker.com/engine/install/
- Docker Compose 2.0+
- 4GB RAM, 2GB disk space

---

### **CÁCH 2A: Docker Desktop (Windows/Mac)**

#### **Bước 1: Cài Docker Desktop**
1. Download từ https://www.docker.com/products/docker-desktop
2. Chạy installer, chọn WSL 2 backend (Windows)
3. Restart máy

#### **Bước 2: Tạo Dockerfile**
Tạo file `Dockerfile` ở root repo:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Cài đặt dependencies hệ thống
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium-browser \
    chromium-chromedriver \
    && rm -rf /var/lib/apt/lists/*

# Copy code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m playwright install

# Copy app
COPY . .

# Expose ports
EXPOSE 5000 5678

# Run dashboard
CMD ["python", "-m", "app.dashboard"]
```

#### **Bước 3: Tạo docker-compose.yml**
```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./profiles:/app/profiles
    env_file:
      - .env
    restart: unless-stopped
    environment:
      FLASK_ENV: production
      PYTHONUNBUFFERED: 1

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    env_file:
      - .env
    restart: unless-stopped

volumes:
  n8n_data:
    driver: local
```

#### **Bước 4: Chạy Docker**
```bash
# 1. Khởi động containers
docker-compose up -d

# 2. Kiểm tra status
docker-compose ps

# 3. Xem logs
docker-compose logs -f dashboard

# 4. Truy cập:
# Dashboard: http://localhost:5000
# n8n:      http://localhost:5678
```

#### **Lệnh Hữu Ích (Docker Desktop)**
```bash
# Dừng tất cả
docker-compose down

# Xóa volume (cộ dữ liệu)
docker-compose down -v

# Rebuild image
docker-compose build --no-cache

# Restart container
docker-compose restart dashboard

# SSH vào container
docker exec -it <container-name> bash

# Xem logs real-time
docker-compose logs -f
```

---

### **CÁCH 2B: Docker trên VPS (Linux)**

#### **Bước 1: SSH vào VPS**
```bash
ssh user@your-vps-ip
```

#### **Bước 2: Cài Docker & Docker Compose**
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y docker.io docker-compose

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user vào docker group (không cần sudo)
sudo usermod -aG docker $USER
newgrp docker
```

#### **Bước 3: Clone Repo**
```bash
cd /home/username/projects
git clone <repo-url> social-auto-bot
cd social-auto-bot
```

#### **Bước 4: Tạo .env cho VPS**
```bash
# Copy mẫu
cp .env.example .env

# Sửa .env
nano .env

# Thêm:
FACEBOOK_EMAIL=your-email@gmail.com
FACEBOOK_PASSWORD=your-password
NOTION_API_KEY=your-key
VPS_DOMAIN=your-domain.com
```

#### **Bước 5: Chạy với Traefik + SSL (Optional)**
Tạo `docker-compose.prod.yml` cho production:

```yaml
version: '3.8'

services:
  traefik:
    image: traefik:latest
    restart: unless-stopped
    command:
      - "--api=true"
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
      - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email=${SSL_EMAIL}"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - traefik_data:/letsencrypt
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - traefik

  dashboard:
    build: .
    restart: unless-stopped
    networks:
      - traefik
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dashboard.rule=Host(`${VPS_DOMAIN}`)"
      - "traefik.http.routers.dashboard.entrypoints=web,websecure"
      - "traefik.http.routers.dashboard.tls.certresolver=letsencrypt"
      - "traefik.http.services.dashboard.loadbalancer.server.port=5000"
    volumes:
      - ./data:/app/data
      - ./profiles:/app/profiles
    env_file:
      - .env
    environment:
      PYTHONUNBUFFERED: 1
      FLASK_ENV: production

  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    networks:
      - traefik
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.n8n.rule=Host(`n8n.${VPS_DOMAIN}`)"
      - "traefik.http.routers.n8n.entrypoints=web,websecure"
      - "traefik.http.routers.n8n.tls.certresolver=letsencrypt"
      - "traefik.http.services.n8n.loadbalancer.server.port=5678"
    volumes:
      - n8n_data:/home/node/.n8n
    env_file:
      - .env
    environment:
      N8N_HOST: "n8n.${VPS_DOMAIN}"
      N8N_PROTOCOL: "https"

volumes:
  n8n_data:
    driver: local
  traefik_data:
    driver: local

networks:
  traefik:
    driver: bridge
```

#### **Bước 6: Chạy Production**
```bash
# Khởi động
docker-compose -f docker-compose.prod.yml up -d

# Xem logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart một service
docker-compose -f docker-compose.prod.yml restart dashboard
```

#### **Truy Cập VPS**
```
Dashboard: https://your-domain.com
n8n:       https://n8n.your-domain.com
```

---

## 🔧 Tương Đương: Native vs Docker

| Task | Native | Docker |
|------|--------|--------|
| **Chạy** | `DASHBOARD.bat` | `docker-compose up -d` |
| **Dừng** | Đóng cửa sổ | `docker-compose down` |
| **Xem logs** | Console màn hình | `docker-compose logs -f` |
| **SSH** | Local shell | `docker exec -it <name> bash` |
| **Backup data** | Copy `data/` folder | `docker volume ls` + backup volumes |
| **Update** | `git pull` + restart | `git pull` + `docker-compose build` |
| **Scale** | N/A | `docker-compose up -d --scale dashboard=3` |

---

## ⚠️ Lưu Ý Quan Trọng

### **Native**
- ✅ Đơn giản, nhanh
- ❌ Khó backup dữ liệu
- ❌ Dependency conflicts (Python versions)
- ❌ Chỉ chạy trên máy này

### **Docker**
- ✅ Portable, scalable
- ✅ Dễ backup (volumes)
- ✅ Cô lập môi trường
- ✅ Production-ready
- ❌ Cần học Docker cơ bản
- ❌ Tiêu thụ nhiều tài nguyên

---

## 🎯 Quyết Định: Native hay Docker?

**Chọn NATIVE nếu:**
- Bạn là beginner
- Chạy trên máy cá nhân
- Không cần deploy lên VPS
- Dữ liệu không quan trọng

**Chọn DOCKER nếu:**
- Bạn muốn production-ready
- Dự định deploy lên VPS
- Cần backup/migrate dễ dàng
- Quản lý nhiều services (Playwright + n8n + NCA)

---

## 📞 Troubleshooting

### **Native**
```bash
# Python không tìm được
python --version  # Kiểm tra cài Python chưa

# Lỗi Playwright
python -m playwright install  # Cài Playwright browsers

# Port 5000 đã được dùng
netstat -ano | findstr :5000  # Find PID, kill process
```

### **Docker**
```bash
# Container không khởi động
docker-compose logs dashboard  # Xem chi tiết lỗi

# Port conflict
docker ps  # Kiểm tra containers đang chạy
docker-compose down  # Dừng tất cả

# Permission denied
sudo docker-compose up -d  # Chạy với sudo hoặc add user to docker group

# Out of disk space
docker system prune -a  # Xóa unused images
```

---

## 📚 Tài Liệu Tham Khảo

- Docker Docs: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Traefik: https://traefik.io/traefik/
- n8n Docker: https://docs.n8n.io/hosting/installation/docker/
- Python venv: https://docs.python.org/3/library/venv.html

