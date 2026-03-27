# 🎯 Hướng Dẫn Đăng Bài Facebook Tự Động - Phiên bản Khách Hàng

**Phiên bản:** 1.0 | **Cập nhật:** 2026-03-27 | **Hỗ trợ:** Vietnamese

---

## 📖 Mục Lục

1. [Cài đặt ban đầu](#cài-đặt-ban-đầu)
2. [Đăng nhập Facebook](#đăng-nhập-facebook)
3. [Sử dụng Dashboard](#sử-dụng-dashboard)
4. [Đăng bài thủ công](#đăng-bài-thủ-công)
5. [Lên lịch tự động](#lên-lịch-tự-động)
6. [Xem báo cáo](#xem-báo-cáo)
7. [Troubleshooting](#troubleshooting)

---

## Cài đặt ban đầu

### Bước 1: Chạy setup (chỉ 1 lần)

1. **Mở PowerShell** hoặc Command Prompt
2. **Đi vào thư mục project:**
   ```powershell
   cd "đường_dẫn_thư_mục_này"
   ```
3. **Chạy:**
   ```powershell
   .\CLIENT_SETUP.bat
   ```

> **Chú ý:** Setup sẽ tải ~300MB Chromium, cho phép 5-10 phút tùy tốc độ internet.

**Kết quả:** Màn hình sẽ hiển thị:
```
✓ Setup hoàn thành!

Các bước tiếp theo:
1. Đăng nhập Facebook...
2. Mở Dashboard...
3. Đặt lịch tự động...
```

---

## Đăng nhập Facebook

### Lần đầu (quan trọng!)

1. **Mở PowerShell**
2. **Gõ:**
   ```powershell
   python scripts\fb_client.py login
   ```

3. **Chrome sẽ mở ra** → **Đăng nhập Facebook thủ công**
4. **Sau khi đăng nhập, ĐÓNG TRÌNH DUYỆT**
5. **PowerShell sẽ hiển thị:**
   ```
   ✓ Phiên được lưu. Có thể đóng trình duyệt.
   ```

> **Sau khi này:** Không cần đăng nhập lại, hệ thống nhớ phiên auto.

---

## Sử dụng Dashboard (Đơn giản nhất!)

### Bước 1: Mở Dashboard

Mở PowerShell, gõ:
```powershell
python run_dashboard.py
```

Kết quả:
```
[*] Đang chạy trên: http://127.0.0.1:5000
```

### Bước 2: Mở trình duyệt

- **Vào:** `http://127.0.0.1:5000`
- Hoặc **Ctrl+click** vào link trong PowerShell

### Bước 3: Sử dụng giao diện

| Chức năng | Cách dùng |
|---|---|
| **📝 Đăng Bài Thường** | Nhập text, chọn ảnh/video (tùy chọn), click "Đăng Bài" |
| **🎬 Đăng Reel** | Chọn video, nhập mô tả, click "Đăng Reel" |
| **🔐 Đăng nhập** | Click nút "Đăng nhập", đăng nhập FB ở cửa sổ Chrome |
| **+ Thêm Profile** | Để đăng bài từ nhiều tài khoản FB khác nhau |
| **📊 Lịch sử** | Tự động cập nhật, hiển thị tất cả hoạt động |

**Ví dụ:**
```
Profile: profile_1
Nội dung: "Hôm nay mình rất vui! 😊"
Ảnh: [chọn file]
Chỉ mình tôi: ✓ (được tích)
→ Click "✅ Đăng Bài"
```

---

## Đăng bài thủ común (PowerShell)

### Chỉ text

```powershell
python scripts\fb_client.py post_feed --profile "profile_1" --content "Nội dung bài viết" --private
```

### Với ảnh/video

```powershell
python scripts\fb_client.py post_feed --profile "profile_1" --content "Nội dung" --media "C:\path\to\image.jpg" --private
```

### Công khai (không private)

```powershell
python scripts\fb_client.py post_feed --profile "profile_1" --content "Nội dung" --private
```

Bỏ `--private` để công khai.

### Xem lịch sử hoạt động

```powershell
python scripts\fb_client.py logs --profile "profile_1"
```

---

## Lên lịch tự động

### Mục tiêu
Đặt những bài viết để **chạy tự động vào giờ bạn chỉ định** (không cần mở máy).

### Cách dùng (Menu interactive)

1. **Mở PowerShell**
2. **Gõ:**
   ```powershell
   python scheduler.py
   ```

3. **Menu hiện ra:**
   ```
   ============================================================
     TY AUTOMATION - SCHEDULER MANAGER
   ============================================================

   [1] Add job
   [2] List jobs
   [3] Pause/Resume job
   [4] Remove job
   [5] Start scheduler
   [0] Exit
   ```

### Thêm lịch (Option 1)

```
Choice: 1

Type (feed/reel):
> feed

Profile name:
> profile_1

Time (HH:MM):
> 14:30

Content/Description:
> Xin chào mọi người!

Media path (optional):
> 

Repeat (once/daily/weekly):
> daily

Private (y/n):
> y

[✓] Job added!
```

### Xem danh sách lịch (Option 2)

```
Choice: 2

====================================
ID           Type   Time   Repeat   Status
1234567890   feed   14:30  daily    active
1234567891   reel   16:00  daily    active
====================================
```

### Bắt đầu Scheduler (Option 5)

```
Choice: 5

[✓] Scheduler started. Chi se chay o ['14:30', '16:00']
[!] Ctrl+C de dung

→ Để chạy 24/7, hãy để PowerShell chạy liên tục
```

### Ví dụ: Đặt lịch đăng 2 bài/ngày

**9:00 AM - Bài chào buổi sáng:**
```
Type: feed
Time: 09:00
Content: Chúc mọi người ngày mới tốt lành!
Repeat: daily
```

**18:00 - Reel chiều:**
```
Type: reel
Time: 18:00
Media: C:\Videos\daily_video.mp4
Content: Hôm nay cùng khám phá...
Repeat: daily
```

---

## Xem báo cáo

### Báo cáo hàng ngày (HTML)

1. **Mở PowerShell**
2. **Gõ:**
   ```powershell
   python report_generator.py
   ```

3. **In ra màn hình:**
   ```
   ============================================================
     DAILY SUMMARY
   ============================================================
   
   Date: 2026-03-27
   
   Total Posts: 5
   Success:     5
   Errors:      0
   
   profile_1    | Total:  5 | Success:  5 | Error:  0
   ============================================================
   ```

4. **File HTML được lưu:**
   ```
   Reports/report_20260327.html
   ```

5. **Mở file HTML để xem chi tiết** (mở bằng trình duyệt)

---

## Quản lý nhiều tài khoản

### Thêm profile mới

**Cách 1: Via Dashboard**
- Nhập tên ở mục "Tên profile mới"
- Click "+ Thêm"
- Chọn profile mới
- Click "🔐 Đăng nhập"
- Đăng nhập Facebook từ tài khoản khác

**Cách 2: Via CLI**
- Dashboard sẽ tự tạo khi bạn dùng `--profile "tên_mới"`

### Ví dụ

```powershell
# Đăng bài từ profile_1
python scripts\fb_client.py post_feed --profile "profile_1" --content "..."

# Đăng bài từ profile_2 (khách hàng khác)
python scripts\fb_client.py post_feed --profile "profile_2" --content "..."
```

---

## Troubleshooting

### ❌ "Python không được nhận dạng"

**Nguyên nhân:** Python chưa được thêm vào PATH

**Cách sửa:**
1. Cài Python lại từ: https://www.python.org/downloads
2. **Tích vào** "Add Python to PATH"
3. Restart PowerShell
4. Thử lại

---

### ❌ "Chrome không mở được"

**Nguyên nhân:** Chromium chưa được tải

**Cách sửa:**
```powershell
playwright install chromium
```

---

### ❌ "Lỗi đăng nhập: 'Không tìm thấy phần tử'"

**Nguyên nhân:** Giao diện Facebook thay đổi hoặc bạn chưa đăng nhập

**Cách sửa:**
1. Đăng nhập lại: `python scripts\fb_client.py login`
2. Chắc chắn bạn ĐÓNG trình duyệt sau khi đăng nhập
3. Thử lại

---

### ❌ "Dashboard không kết nối (localhost:5000)"

**Nguyên nhân:** Cổng 5000 bị dùng

**Cách sửa:**
1. Sửa file `.env`:
   ```
   FLASK_PORT=5001
   ```
2. Chạy lại:
   ```powershell
   python run_dashboard.py
   ```
3. Vào: `http://127.0.0.1:5001`

---

### ❌ "Báo cáo trống"

**Nguyên nhân:** Chưa có hoạt động nào hôm nay

**Cách sửa:** Đăng 1 bài rồi chạy báo cáo lại

---

## 🎓 Tips & Tricks

### ✅ Tránh bị Facebook phát hiện là bot

- ✓ Sử dụng `--private` khi test
- ✓ Không đăng bài quá nhanh (hệ thống có delay tự động)
- ✓ Giữa những lần đăng ≥ 1 giờ

### ✅ Sử dụng hiệu quả

- ✓ Lập kế hoạch nội dung trước
- ✓ Dùng Dashboard thay vì CLI (dễ hơn)
- ✓ Đặt lịch vào giờ mà khách hàng thường online

### ✅ Bảo mật

- ✓ Giữ bí mật `.env` file
- ✓ Không chia sẻ thư mục `Profiles/`
- ✓ Chỉ dùng Chrome chính thức (không chạy bản sao khác)

---

## 📞 Cần Giúp?

| Vấn đề | Giải pháp |
|---|---|
| Setup không chạy | Xem lại Python đã cài chưa |
| Dashboard không hiển thị | Check cổng 5000 trong `.env` |
| Đăng bài lỗi | Chạy `python scripts\fb_client.py logs --profile "tên"` để xem chi tiết |
| Scheduler không chạy | Kiểm tra format giờ (HH:MM), VD: 14:30 |
| Báo cáo trống | Đảm bảo đã đăng bài hôm nay |

---

## 🔄 Quy Trình Hàng Ngày

### Sáng
```powershell
python run_dashboard.py
→ Dashboard mở tại http://127.0.0.1:5000
→ Lập kế hoạch bài viết cho hôm nay
```

### Chiều / Tối
```powershell
# (Scheduler đã tự động đăng bài)
python report_generator.py
→ Xem báo cáo màn hình
```

---

**Chúc mừng bạn! 🎉 Hệ thống đã sẵn sàng để tự động hóa Facebook!**

Nếu gặp bất kỳ vấn đề nào, hãy yên tâm - những lỗi thường gặp đều có cách sửa ở mục Troubleshooting.

---

*Last Updated: 2026-03-27*
*Version: 1.0*
