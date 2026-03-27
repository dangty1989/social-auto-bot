# 🚀 Hướng Dẫn Triển Khai cho Nhà Phát Triển

**Phiên bản:** 1.0 | **Mục đích:** Hướng dẫn deploy cho nhiều khách hàng

---

## 📋 Tổng Quan Hệ Thống

### Kiến Trúc

```
┌─────────────────────────────────────────────────┐
│  Khách Hàng (Không tech)                        │
│  ├── Machine 1: Đăng bài tự động                │
│  ├── Machine 2: Dashboard Web + Scheduler       │
│  └── Machine 3: Reports + Analytics             │
└─────────────────────────────────────────────────┘
                        ▲
                        │ (HTTP)
                   Thư mục này
        (CLIENT_DIST - sao cho khách)
```

### Các Thành Phần

| File | Mục đích | Khách dùng? |
|---|---|---|
| `CLIENT_SETUP.bat` | Cài đặt toàn bộ 1-click | ✅ Yes |
| `run_dashboard.py` | Web UI đăng bài | ✅ Yes (Easy) |
| `scheduler.py` | Lên lịch tự động | ✅ Yes |
| `report_generator.py` | Báo cáo hàng ngày | ✅ Yes |
| `scripts/fb_client.py` | CLI nâng cao | ⚠️ Optional |
| `HUONG_DAN_KHACH_HANG.md` | Tài liệu chi tiết | ✅ Yes |

---

## 🎯 Quy Trình Deployment

### 1️⃣ Chuẩn Bị Bộ Cài

```bash
# Copy toàn bộ thư mục FB_Agency_Dist cho khách
copy-item -r FB_Agency_Dist "C:\CLIENT_PACKS\client_tenKhach"
```

**Cấu trúc sẽ gửi cho khách:**
```
CLIENT_tenKhach/
├── CLIENT_SETUP.bat              # ← Bắt đầu từ đây
├── run_dashboard.py              # Dashboard
├── scheduler.py                  # Lên lịch
├── report_generator.py           # Báo cáo
├── .env.example                  # Template cấu hình
├── QUICK_START.md                # Bắt đầu nhanh
├── HUONG_DAN_KHACH_HANG.md       # Hướng dẫn chi tiết
├── requirements.txt              # Dependencies
└── scripts/
    └── fb_client.py              # Core engine
```

---

### 2️⃣ Cài Đặt tại Khách

**Khách chạy:**
```powershell
.\CLIENT_SETUP.bat
```

**Script sẽ:**
- ✅ Kiểm tra Python (yêu cầu)
- ✅ Tạo thư mục cần thiết (Profiles, Logs, Reports)
- ✅ Cài Playwright + Chromium
- ✅ Tạo .env tự động
- ✅ Hướng dẫn tiếp theo

---

### 3️⃣ Khách Đăng Nhập Facebook

**Khách chạy:**
```powershell
python scripts\fb_client.py login
```

**Kết quả:** Phiên lưu trong `Profiles/`, không cần lại

---

### 4️⃣ Khách Sử Dụng

#### **Cách 1: Dashboard (Dễ nhất)**
```powershell
python run_dashboard.py
# → http://127.0.0.1:5000
```

#### **Cách 2: CLI (Nâng cao)**
```powershell
python scripts\fb_client.py post_feed --profile "p1" --content "..." --private
```

#### **Cách 3: Lên Lịch (Tự động)**
```powershell
python scheduler.py
# → Menu interactive
# → Add job → 14:30 daily
# → Start scheduler
```

---

## 📊 Báo Cáo & Monitoring

### Hàng Ngày

```powershell
python report_generator.py
```

**Output:**
- Màn hình: Summary
- File: `Reports/report_20260327.html`

### Email Reports (Tùy chọn)

1. **Sửa .env:**
   ```env
   REPORT_EMAIL_TO=khach@gmail.com
   REPORT_EMAIL_FROM=bot@gmail.com
   REPORT_EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```

2. **Với Gmail App Password:**
   - Vào: https://myaccount.google.com/apppasswords
   - Lấy password đặc biệt 16 ký tự

3. **Schedule gửi:**
   - Cron job gọi `python report_generator.py --send-email` hàng ngày 20:00

---

## 🔧 Cấu Hình Nâng Cao

### Nhiều Tài Khoản Facebook

```powershell
# Profile 1
python scripts\fb_client.py login --profile "tk_facebook_1"

# Profile 2
python scripts\fb_client.py login --profile "tk_facebook_2"

# Dashboard sẽ hiển thị dropdown các profiles
python run_dashboard.py
```

### Tùy Chỉnh Cổng

**Nếu cổng 5000 bị dùng:**

```bash
# .env
FLASK_PORT=5001
```

### Sử dụng n8n (Workflow Automation)

**Kích hoạt từ n8n:**
```bash
# n8n HTTP node
GET http://127.0.0.1:5000/api/post/feed
{
  "profile": "profile_1",
  "content": "{{ $node.previous.data.post }}",
  "private": true
}
```

---

## 🛡️ Bảo Mật

### Khôi Phục Mật Khẩu Facebook

Nếu khách quên hoặc muốn đặt lại:

```powershell
# Xóa phiên cũ
Remove-Item -r "Profiles\profile_1"

# Đăng nhập lại
python scripts\fb_client.py login --profile "profile_1"
```

### Backup Profiles

```bash
# Sao lưu phiên đang nhập
copy-item -r Profiles "Profiles_backup_$(date)"
```

### Không chia sẻ:
- ❌ Thư mục `Profiles/` (chứa cookies)
- ❌ File `.env` (chứa config)
- ❌ Thư mục `Schedules/` (chứa job definitions)

---

## 🐛 Troubleshooting Deployment

### ❌ "Setup.bat lỗi"

**Gợi ý:**
```powershell
# Kiểm tra Python
python --version

# Nếu lỗi → cài lại Python từ https://python.org
# Nhớ tích "Add Python to PATH"
```

### ❌ "Chrome không mở"

**Gợi ý:**
```powershell
# Tải Playwright
playwright install chromium

# Hoặc setup lại
.\CLIENT_SETUP.bat
```

### ❌ "Dashboard lỗi"

**Gợi ý:**
```powershell
# Cổng bị dùng?
netstat -ano | findstr :5000

# Nếu có process → kill hoặc đổi cổng
# Sửa .env: FLASK_PORT=5001
```

### ❌ "Logs trống"

**Nguyên nhân:** Chưa có hoạt động hôm nay
```powershell
# Test đăng bài
python scripts\fb_client.py post_feed --profile "p1" --content "test" --private

# Rồi chạy báo cáo
python report_generator.py
```

---

## 📈 Monitoring Khách Hàng (Từ Phía Bạn)

### Kinh doanh: SLA Tracking

| Metric | Target | Tool |
|---|---|---|
| Uptime | 99% | Cron check |
| Posts/day | ≥ N | reports.json |
| Errors/week | ≤ M | log analysis |

### Kỹ Thuật: Health Check

```python
# (Tùy chọn) check_health.py
import json, os
from datetime import datetime, timedelta

logs_dir = "./Logs"
today = datetime.now().date()

for profile_log in os.listdir(logs_dir):
    logs = json.load(open(f"{logs_dir}/{profile_log}"))
    today_logs = [l for l in logs if datetime.fromisoformat(l['timestamp']).date() == today]
    
    success = len([l for l in today_logs if l['status'] == 'success'])
    errors = len([l for l in today_logs if l['status'] == 'error'])
    
    print(f"{profile_log}: {success} success, {errors} errors")
    
    if errors > 5:
        # Alert: Too many errors today
        print(f"⚠️ ALERT: {profile_log} has {errors} errors!")
```

---

## 📦 Deploy ke Multiple Customers

### Batch Deployment

```powershell
# deploy.ps1
$customers = @("client_1", "client_2", "client_3")

foreach ($customer in $customers) {
    $path = "C:\CLIENT_PACKS\$customer"
    
    # Copy codebase
    copy-item -r FB_Agency_Dist $path -force
    
    # Setup
    cd $path
    .\CLIENT_SETUP.bat
    
    # Tạo shortcut
    $shell = New-Object -com "WScript.Shell"
    $shortcut = $shell.CreateShortcut("$path\Dashboard.lnk")
    $shortcut.TargetPath = "python"
    $shortcut.Arguments = "run_dashboard.py"
    $shortcut.WorkingDirectory = $path
    $shortcut.Save()
}
```

---

## 🚀 Best Practices

### ✅ Checklist Deployment

- [ ] Copy codebase đầy đủ
- [ ] Khách chạy CLIENT_SETUP.bat thành công
- [ ] Khách đăng nhập Facebook 1 lần
- [ ] Test: Đăng bài qua Dashboard
- [ ] Test: Lên lịch 1 job
- [ ] Test: Xem báo cáo
- [ ] Khách biết cách troubleshoot (doc HUONG_DAN)
- [ ] Backup Profiles folder nếu cần

### ✅ Support Strategy

**Tier 1 (Self-service):**
- QUICK_START.md cho khách mới
- HUONG_DAN_KHACH_HANG.md chi tiết
- Troubleshooting section

**Tier 2 (Email support):**
- Ghi log lỗi (fb_client.py tự ghi)
- Khách gửi logs để bạn phân tích

**Tier 3 (Remote access):**
- TeamViewer / AnyDesk để debug trực tiếp

---

## 📞 Contact & Updates

- **Version:** 1.0 (2026-03-27)
- **Python:** 3.9+
- **Browser:** Chrome/Chromium
- **OS:** Windows 10+

---

**Bây giờ bạn có thể deploy cho nhiều khách! 🎉**
