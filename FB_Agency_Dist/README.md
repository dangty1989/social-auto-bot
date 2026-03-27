# 📱 TY AUTOMATION - Hệ Thống Đăng Bài Facebook Tự Động

**Công cụ mạnh mẽ giúp bạn đăng bài trên Facebook cá nhân một cách tự động.**
- ⏱️ Hẹn giờ đăng bài (hàng ngày, hàng tuần)
- 🎬 Hỗ trợ Feed + Reel
- 📊 Báo cáo hoạt động hàng ngày
- 👥 Quản lý nhiều tài khoản Facebook
- 🌐 Giao diện web đơn giản (không cần dòng lệnh)

---

## 🚀 Bắt Đầu Nhanh (2 Bước)

### **Lần Đầu Tiên**
1. **Nhấp đúp vào `SETUP.bat`** → Chượng trình sẽ tự cài đặt (mất 5-10 phút)
2. **Nhấp đúp vào `DASHBOARD.bat`** → Trình duyệt sẽ mở giao diện

### **Hàng Ngày**
- **Nhấp đúp `DASHBOARD.bat`** → Viết bài → Nhấn "Đăng Bài" → Xong!

---

## 📂 Cấu Trúc Thư Mục

```
social-auto-bot/
├── SETUP.bat              Cài đặt (chạy 1 lần lần đầu)
├── DASHBOARD.bat          Mở giao diện web (chạy hàng ngày)
├── README.md              Hướng dẫn này
├── requirements.txt       Thư viện cần thiết
├── .env.example           Mẫu cấu hình
│
├── app/                   Mã lập trình (không cần chỉnh sửa)
│   ├── engine.py          Động cơ Facebook (Playwright + Automation)
│   ├── dashboard.py       Giao diện web (Flask)
│   ├── scheduler.py       Hẹn giờ đăng bài
│   ├── report.py          Tạo báo cáo hàng ngày
│   ├── verify.py          Kiểm tra lỗi hệ thống
│   └── templates/         Mã HTML giao diện
│
├── docs/                  Tài liệu bổ sung
│   ├── HUONG_DAN_KHACH_HANG.md
│   └── DEPLOYMENT_GUIDE.md
│
└── data/                  Dữ liệu (tự động tạo - không cần động)
    ├── profiles/          Lưu phiên đăng nhập Facebook
    ├── logs/              Lịch sử hoạt động
    ├── reports/           Báo cáo HTML
    └── schedules/         Lịch hẹn giờ đăng bài
```

---

## ✨ Các Tính Năng Chính

| Tính Năng | Mô Tả |
|-----------|-------|
| **📝 Đăng Bài Feed** | Đăng Text + Ảnh/Video lên Feed cá nhân |
| **🎬 Đăng Reel** | Đăng video ngắn (Reels) |
| **⏰ Hẹn Giờ** | Đăng tự động vào thời gian bạn chỉ định (1 lần, hàng ngày, hàng tuần) |
| **📊 Báo Cáo** | Thống kê hoạt động hàng ngày (HTML + Email) |
| **👥 Nhiều Tài Khoản** | Quản lý và đăng bài trên nhiều tài khoản Facebook |
| **🔐 Bảo Mật** | Lưu phiên đăng nhập an toàn (không cần nhập mật khẩu mỗi lần) |

---

## 💻 Sử Dụng Dòng Lệnh (Advanced)

Mở **Command Prompt** hoặc **PowerShell** trong thư mục và chạy:

```bash
# Đăng nhập Facebook (lần đầu)
python app/engine.py login --profile profile_1

# Đăng bài Feed
python app/engine.py post_feed --profile profile_1 --content "Nội dung bài viết"

# Đăng Reel
python app/engine.py post_reel --profile profile_1 --media video.mp4 --content "Mô tả video"

# Quản lý hẹn giờ
python app/scheduler.py

# Tạo báo cáo
python app/report.py

# Kiểm tra hệ thống
python app/verify.py
```

---

## 🔗 Tích Hợp N8N (Tự Động Hoá 100%)

**N8N là gì?** Công cụ workflow automation không cần code - kết nối nhiều ứng dụng lại với nhau.

### Bạn Có Thể Làm:

✅ Tự động đăng bài từ **Google Sheets** hàng ngày  
✅ Gửi báo cáo qua **Email / Slack / Telegram** tự động  
✅ Kết hợp với **Database** để quản lý nội dung  
✅ Hẹn giờ phức tạp (đăng vào thứ 2-5 lúc 8h sáng, v.v.)  

### Quick Start:

```bash
# Cài N8N
npm install -g n8n

# Chạy N8N
n8n start

# Mở: http://127.0.0.1:5678
```

👉 **[Hướng Dẫn Chi Tiết: N8N + Playwright](docs/N8N_INTEGRATION.md)**

---

## 🤖 Hệ Thống Tự Động Hoá Nâng Cao (N8N + AI + Playwright + NCA)

**Muốn xây dựng hệ thống professional?** Kết hợp:
- **N8N**: Workflow automation (lên lịch, control flow)
- **AI (Perplexity)**: Phân tích & tạo nội dung thông minh
- **Playwright**: Tự động hoá Facebook
- **NCA Toolkit**: Xử lý media (video, ảnh, audio, captions)

### Các Tình Huống:

✅ **YouTube Curator**: Tìm video hot hôm nay → Tạo captions → Đăng Facebook auto  
✅ **Batch Posting**: Đọc content từ Google Sheets → AI enhance → NCA process → Post  
✅ **Smart Analytics**: Perplexity phân tích tâm lý khán giả → Đăng bài lúc best time  
✅ **Multi-Channel**: Post cùng lúc lên Facebook, Instagram, Telegram  

👉 **[Hướng Dẫn Hoàn Chỉnh: Advanced Automation System](docs/ADVANCED_AUTOMATION_SYSTEM.md)**

---

## ⚙️ Cấu Hình

### Sao chép mẫu cấu hình
1. Sao chép file `.env.example` → Đổi tên thành `.env`
2. Mở `.env` bằng Notepad → Sửa các giá trị:

```
# Đường dẫn dữ liệu
FB_PROFILES_DIR=./data/profiles
LOGS_DIR=./data/logs
REPORTS_DIR=./data/reports
SCHEDULES_DIR=./data/schedules

# Giao diện web
FLASK_PORT=5000          (cổng, thay đổi nếu bị xung đột)
FLASK_HOST=127.0.0.1     (chỉ chạy ở máy local)

# Email báo cáo (tùy chọn)
REPORT_EMAIL_TO=your_email@gmail.com
REPORT_EMAIL_FROM=automation_account@gmail.com
REPORT_EMAIL_PASSWORD=xxxx xxxx xxxx xxxx  (App Password từ Gmail)
```

---

## 🛠️ Xử Lý Lỗi

| Lỗi | Giải Pháp |
|-----|----------|
| **"Python không tìm thấy"** | Cài Python 3.8+ từ python.org → Tick "Add Python to PATH" |
| **"Dashboard không mở"** | Kiểm tra port 5000 có bị chiếm không → Chạy lại DASHBOARD.bat |
| **"Đăng bài thất bại"** | Đăng nhập lại Facebook (bấm nút "Đăng Nhập" trên Dashboard) |
| **"Chrome không mở"** | Chạy: `playwright install chromium` |

### Kiểm Tra Toàn Bộ Hệ Thống
```
python app/verify.py
```

---

## 📖 Tài Liệu Thêm

- [Hướng Dẫn Chi Tiết Cho Khách Hàng](docs/HUONG_DAN_KHACH_HANG.md)
- [Hướng Dẫn Triển Khai](docs/DEPLOYMENT_GUIDE.md)
- [🔗 Kết Hợp N8N + Playwright (Advanced)](docs/N8N_INTEGRATION.md) - Tự động hóa toàn bộ qua N8N workflow

---

## 📝 Lưu Ý Quan Trọng

✅ **An toàn:**
- Phiên đăng nhập được lưu an toàn (Chrome profile)
- Mật khẩu KHÔNG được lưu trữ
- Code hoàn toàn minh bạch (bạn có thể xem toàn bộ)

⚠️ **Tuân thủ:**
- Chỉ sử dụng cho tài khoản Facebook cá nhân của bạn
- Tuân thủ Điều Khoản Dịch Vụ của Facebook
- Không spam, không gửi mail rác

---

## 🤝 Hỗ Trợ & Phản Hồi

Nếu gặp lỗi:
1. Chạy `python app/verify.py` để kiểm tra hệ thống
2. Xem thư mục `data/logs/` để đọc lịch sử lỗi
3. Kiểm tra file `docs/HUONG_DAN_KHACH_HANG.md`

---

## 📄 License

Miễn phí sử dụng (MIT License)

---

**Chúc bạn sử dụng thành công! 🎉**
