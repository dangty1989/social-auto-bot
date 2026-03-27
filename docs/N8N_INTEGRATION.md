# 🔗 Hướng Dẫn: Kết Hợp N8N + Playwright

**Mục tiêu:** Dùng N8N workflow để tự động hoá hoàn toàn quá trình đăng bài Facebook qua Playwright.

---

## 📋 Tổng Quan

### Kiến Trúc

```
N8N Workflow
    ↓
  [Trigger] (Cron Job / Webhook / Manual)
    ↓
  [Get Data] (Lấy nội dung từ DB/Sheet/File)
    ↓
  [Call Python Script] (Gọi app/engine.py qua HTTP/CLI)
    ↓
  [Wait for Result] (Chờ Playwright hoàn thành)
    ↓
  [Send Report] (Gửi báo cáo qua Email/Telegram)
    ↓
  [Log & Archive] (Lưu nhật ký)
```

### Lợi Ích

✅ **Tự động hoá 100%** - Không cần click button  
✅ **Hẹn giờ chính xác** - N8N cron job scheduling  
✅ **Kết hợp nhiều nguồn** - Google Sheets, Database, API  
✅ **Thông báo tức thì** - Email, Slack, Telegram  
✅ **Lịch sử đầy đủ** - Audit log mọi thao tác  

---

## 🚀 Cách Cài Đặt N8N

### 1. Cài Đặt N8N Locally

```bash
# Cài NODE.js trước (nếu chưa có)
# Từ https://nodejs.org (LTS version)

# Cài N8N điểm toàn cầu
npm install -g n8n

# Chạy N8N
n8n start
```

**N8N sẽ hoạt động tại:** `http://127.0.0.1:5678`

### 2. (Tùy Chọn) Chạy N8N bằng Docker

```bash
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### 3. Cấu Hình N8N

Vào `http://127.0.0.1:5678`:
1. Tạo tài khoản admin
2. Đặt tên workspace
3. Bắt đầu tạo workflow

---

## 📊 Thiết Kế N8N Workflow

### Scenario 1: Đăng Bài Từ Google Sheets (Hàng Ngày)

#### **Nodes cần thiết:**

```
[1] Cron Trigger
    └─ Chạy mỗi ngày lúc 8h sáng
    
[2] Google Sheets
    └─ Lấy row mới từ Sheets (profile, nội dung, ảnh)
    
[3] HTTP Request (Gọi Python Script)
    ├─ URL: http://localhost:5000/api/post/feed
    ├─ Method: POST
    ├─ Body: {
    │    "profile": sheet.profile,
    │    "content": sheet.content,
    │    "media": sheet.media_url
    │  }
    
[4] Wait
    └─ Chờ 10 giây cho Playwright thực thi
    
[5] Send Email
    └─ Gửi báo cáo kết quả cho bạn
    
[6] Update Sheets
    └─ Đánh dấu "Đã đăng" trong Sheets
```

---

## 🛠️ Cài Đặt Từng Node

### **Node 1: Trigger - Cron Job**

```
Node Type: Cron
Schedule: 0 8 * * * (8h sáng mỗi ngày)
Timezone: Asia/Ho_Chi_Minh
```

### **Node 2: Google Sheets**

```
Node Type: Google Sheets
Operation: Get All Rows
Spreadsheet ID: [Copy từ URL Sheets]
Sheet: Nội Dung Đăng Bài
Range: A2:E (từ hàng 2 trở đi)

Columns:
  A: profile_name
  B: content
  C: media_url
  D: status (để trống)
  E: posted_time (để trống)
```

**Định dạng Google Sheets:**

| profile_name | content | media_url | status | posted_time |
|---|---|---|---|---|
| profile_1 | Nội dung bài 1 | https://...jpg | | |
| profile_2 | Nội dung bài 2 | https://...mp4 | | |

### **Node 3: HTTP Request - Gọi API**

```
Node Type: HTTP Request
Method: POST
URL: http://127.0.0.1:5000/api/post/feed

Authentication: None (hoặc Basic Auth nếu cần)

Body (raw JSON):
{
  "profile": "{{ $node['Google Sheets'].json.profile_name }}",
  "content": "{{ $node['Google Sheets'].json.content }}",
  "private": "true"
}

Headers:
  Content-Type: application/json
```

**Nếu có media (File Upload):**

```
Khi gửi file, tạo FormData:
  - profile: profile_1
  - content: Nội dung
  - media: [file binary]
```

### **Node 4: Wait**

```
Node Type: Wait
Wait: 30 seconds (chờ Playwright hoàn thành)
```

### **Node 5: Send Email**

```
Node Type: Gmail
To: your_email@gmail.com
Subject: ✅ Đã đăng bài Facebook
Body:
---
Hôm nay đã đăng bài thành công:
- Profile: {{ $node['Google Sheets'].json.profile_name }}
- Nội dung: {{ $node['Google Sheets'].json.content }}
- Thời gian: {{ now().format('HH:mm:ss') }}

Logs: http://127.0.0.1:5000/api/logs?profile={{ $node['Google Sheets'].json.profile_name }}
---
```

### **Node 6: Update Google Sheets**

```
Node Type: Google Sheets
Operation: Update
Spreadsheet ID: [Same]
Sheet: Nội Dung Đăng Bài

Update Data:
{
  "range": "D{{ $node['Google Sheets'].json.__row }}",
  "value": "Đã đăng"
}

{
  "range": "E{{ $node['Google Sheets'].json.__row }}",
  "value": "{{ now().format('HH:mm:ss') }}"
}
```

---

## Scenario 2: Hẹn Giờ Hàng Loạt (Advanced)

Nếu muốn **N8N gọi Python CLI** thay vì HTTP:

### **Node: Execute Command**

```
Node Type: Execute Command
Command: python
Arguments: [
  "{{ env.FB_AUTOMATION_PATH }}/app/scheduler.py",
  "--profile", "{{ $node['Database'].json.profile }}",
  "--time", "{{ $node['Database'].json.scheduled_time }}"
]
```

---

## 🔐 Bảo Mật

### Lưu Biến Môi Trường N8N

**N8N > Settings > Environment Variables:**

```
FB_API_URL=http://127.0.0.1:5000
FB_AUTOMATION_PATH=f:\DangTy - Automation\FB_Agency_Dist
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
SHEETS_ID=1a2b3c4d5e6f7g8h9i0j
```

**Dùng trong Workflow:**

```
{{ env.FB_API_URL }}/api/post/feed
```

### Mã Hóa Credentials

Trong HTTP Request, dùng **N8N Credentials**:
1. **New Credential** → Gmail OAuth2
2. **New Credential** → Google Sheets OAuth2
3. **New Credential** → Basic Auth (nếu cần)

---

## 📊 Ví Dụ Workflow JSON

Bạn có thể import bằng cách copy JSON này:

```json
{
  "nodes": [
    {
      "parameters": {
        "rule": "everyDayFixedTime",
        "hour": 8,
        "minute": 0,
        "timezone": "Asia/Ho_Chi_Minh"
      },
      "name": "Cron - 8h Sáng",
      "type": "n8n-nodes-base.cron",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "operation": "getAll",
        "spreadsheetId": "{{ env.SHEETS_ID }}",
        "sheetName": "Posts",
        "range": "A2:E"
      },
      "name": "Lấy Dữ Liệu Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 3,
      "position": [450, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "{{ env.FB_API_URL }}/api/post/feed",
        "sendBody": true,
        "bodyContentType": "json",
        "body": {
          "profile": "={{ $node['Lấy Dữ Liệu Sheets'].json.profile }}",
          "content": "={{ $node['Lấy Dữ Liệu Sheets'].json.content }}",
          "private": true
        }
      },
      "name": "Gọi API Đăng Bài",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [650, 300]
    }
  ],
  "connections": {
    "Cron - 8h Sáng": {
      "output": [["default", []]]
    }
  }
}
```

---

## 🚨 Xử Lý Lỗi

### Try-Catch Node

```
[Main Flow]
    ↓
[Try Block: HTTP Request]
    ├─ Success → [Send Success Email]
    └─ Error → [Error Handling]
              └─ [Send Error Email]
              └─ [Log to Database]
```

**Setup Error Handler:**

```
Node Type: Switch
Condition: Check if previous node failed
  ├─ If Success: Route to Success Email
  └─ If Error: Route to Error Email
```

---

## 📈 Theo Dõi & Báo Cáo

### Dashboard N8N

1. Vào **Workflows** → Chọn workflow
2. Xem **Executions Log**
3. Kiểm tra **Success/Failure Rate**
4. Export data sang Google Sheets để phân tích

---

## ⚡ Thủ Thuật Nâng Cao

### 1. Loop Through Multiple Profiles

```
[Get All Profiles from DB]
    ↓
[Loop: For Each Profile]
    ├─ [Call app/engine.py --profile $item]
    ├─ [Wait 10s]
    └─ [Log Result]
```

### 2. Conditional Scheduling

```
[Get Schedule from Database]
    ↓
[If time matches NOW]
    ├─ YES → [Call Engine]
    └─ NO → [Wait & Check Again]
```

### 3. Multi-Channel Notifications

```
[Post Success]
    ├─ [Send Email]
    ├─ [Send Telegram Message]
    ├─ [Send Slack Message]
    └─ [Update Google Sheets]
```

---

## 🔗 Kết Nối với Hệ Thống Hiện Tại

### N8N ↔ Dashboard Flask

**Cách 1: N8N Gọi Flask API (Khuyến Nghị)**

```
N8N HTTP Request → http://127.0.0.1:5000/api/post/feed ← Flask Dashboard
```

**Cách 2: Flask Webhook Thông Báo Cho N8N**

```
Flask → Gọi N8N Webhook → N8N triggers follow-up actions
```

### N8N ↔ Scheduler.py

```
N8N → Execute Command → python app/scheduler.py
```

---

## 📚 Tài Liệu Liên Quan

- [N8N Documentation](https://docs.n8n.io/)
- [N8N Nodes Reference](https://docs.n8n.io/nodes/nodes-library/)
- [Google Sheets Node](https://docs.n8n.io/nodes/n8n-nodes-base.googleSheets/)
- [HTTP Request Node](https://docs.n8n.io/nodes/n8n-nodes-base.httpRequest/)

---

## 🎯 Quick Start: 5 Phút Setup

1. **Cài N8N:** `npm install -g n8n` → `n8n start`
2. **Tạo Workflow:** Click "+" → Drag Cron node
3. **Add HTTP Node:** Link tới `http://localhost:5000/api/post/feed`
4. **Thêm Email Node:** Thông báo kết quả
5. **Active Workflow:** Click "Activate"

Xong! N8N sẽ tự động đăng bài theo lịch hàng ngày.

---

**Chúc bạn thành công với N8N + Playwright! 🚀**
