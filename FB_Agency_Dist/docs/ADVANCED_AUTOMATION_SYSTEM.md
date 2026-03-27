# 🚀 Hướng Dẫn: Kết Hợp N8N + AI + Playwright + NCA Toolkit

**Mục tiêu:** Xây dựng hệ thống tự động hoá toàn diện cho Facebook Marketing với:
- **N8N**: Workflow automation (lên lịch, kích hoạt, xử lý luồng)
- **AI (Perplexity)**: Phân tích, tạo nội dung thông minh
- **Playwright**: Tự động hoá trình duyệt (đăng bài Facebook)
- **NCA Toolkit**: Xử lý media (video, ảnh, audio)

---

## 📊 Kiến Trúc Hệ Thống Tổng Thể

```
┌─────────────────────────────────────────────────────────────────┐
│                    N8N WORKFLOW ORCHESTRATOR                    │
│  (Cron, Control Flow, Conditional Logic, Error Handling)        │
└────────┬────────────────────────────────────────────────────────┘
         │
    ┌────┴─────────────────────┬────────────────────┬─────────────┐
    │                          │                    │             │
    ▼                          ▼                    ▼             ▼
┌──────────────┐        ┌─────────────┐     ┌──────────────┐  ┌──────────┐
│  AI/Perplexity│       │  Google     │    │  Database/   │  │ S3/Cloud │
│ (Content Gen)│       │  Sheets     │    │  JSON Files  │  │ Storage  │
│              │       │ (Data Source)   │              │  │          │
└──────┬───────┘       └────────┬────┘    └──────┬───────┘  └──────────┘
       │                        │               │
       │ Analyze & Summarize    │ Fetch Content │ Get Config
       │                        │               │
       └────────────┬──────────┬┴──────────┬─────┘
                    │          │          │
                   ▼          ▼          ▼
            ┌─────────────────────────────────┐
            │   N8N MAIN PROCESSING NODE     │
            │  (HTTP Request, Conditions,    │
            │   Data Transformation)         │
            └────────┬──────────────────┬────┘
                     │                  │
        ┌────────────┘                  └──────────────┐
        │                                               │
        ▼                                               ▼
┌──────────────────────────┐               ┌────────────────────────┐
│   NCA TOOLKIT PIPELINE   │               │  FLASK API BRIDGE      │
│ ┌──────────────────────┐ │               │ ┌────────────────────┐ │
│ │ Download YouTube     │ │               │ │ app/engine.py      │ │
│ │ Extract Thumbnail    │ │               │ │ (Playwright Engine)│ │
│ │ Transcribe/Translate │ │               │ │ POST /api/post/*   │ │
│ │ Create Captions      │ │               │ │                    │ │
│ │ Convert Format       │ │               │ └────┬───────────────┘ │
│ └──────────────────────┘ │               │      │                 │
└────────┬─────────────────┘               │      │                 │
         │                                 │      │                 │
         │ Enhanced Media                  │      │ Login & Post    │
         │                                 │      │                 │
         └─────────────────────┬───────────┘      │                 │
                               │                  │                 │
                               ▼                  ▼                 │
                    ┌──────────────────────────────────┐            │
                    │     FACEBOOK AUTOMATION          │            │
                    │  (Persistent Chrome Profiles)    │            │
                    │ • Đăng feed, reels              │            │
                    │ • Thêm ảnh/video               │            │
                    │ • Với media từ NCA Toolkit      │            │
                    └──────────┬───────────────────────┘            │
                               ▼                                    │
                    ┌──────────────────────────────────┐            │
                    │     LOG & NOTIFICATION          │            │
                    │ • JSON logs (app/logs/)         │            │
                    │ • Email/Telegram alerts         │            │
                    │ • Dashboard update              │            │
                    └──────────────────────────────────┘            │
                                                                    │
└────────────────────────── Feedback Loop ───────────────────────┘
```

---

## 🎯 Các Tình Huống Thực Tế

### **Tình Huống 1: Tạo Content Tự Động Từ YouTube + Đăng Facebook**

**Mục tiêu:** 
- Lấy video YouTube hot từ Perplexity
- Tạo thumbnail + captions  
- Đăng lên Facebook tự động

**Workflow:**
```
[Cron Trigger - 9:00 AM]
    ↓
[Perplexity Node]
    └─ Query: "Top videos about [topic] today"
    └─ Output: URLs, description
    ↓
[HTTP → NCA Toolkit: /v1/BETA/media/download]
    └─ Download: thumbnail, metadata
    ↓
[NCA Toolkit: /v1/video/thumbnail + /v1/media/transcribe]
    └─ Extract perfect thumbnail
    └─ Get transcript auto
    ↓
[NCA Toolkit: /v1/video/caption]
    └─ Add Vietnamese captions
    ↓
[HTTP → Flask: /api/post/feed]
    ├─ profile: "my_account"
    ├─ content: Perplexity summary
    ├─ media: NCA processed video
    ↓
[Condition: Success?]
    ├─ YES → Send Telegram: "✅ Đã đăng thành công"
    └─ NO  → Send Email: Error details
```

**N8N Workflow JSON:**
```json
{
  "name": "YouTube -> NCA -> Facebook Auto-Post",
  "nodes": [
    {
      "name": "Cron Trigger",
      "type": "n8n-nodes-base.cron",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {
        "cronExpression": "0 9 * * *"
      }
    },
    {
      "name": "Call Perplexity AI",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [450, 300],
      "parameters": {
        "url": "http://localhost:8000/v1/chat/completions",
        "method": "POST",
        "headers": {
          "Authorization": "Bearer {{ $env.PERPLEXITY_TOKEN }}"
        },
        "body": {
          "model": "pplx-7b-online",
          "messages": [
            {
              "role": "user",
              "content": "Tìm top 3 video YouTube hot hôm nay về kiếm tiền online. Trả về URL, title, description"
            }
          ]
        }
      }
    },
    {
      "name": "Extract URLs",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [650, 300],
      "parameters": {
        "jsCode": "const response = $input.first().json;\nconst content = response.choices[0].message.content;\nconst urls = content.match(https:\\/\\/[^\\s]+/g) || [];\nreturn { urls, summary: content };"
      }
    },
    {
      "name": "Download from NCA Toolkit",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [850, 300],
      "parameters": {
        "url": "http://localhost:8080/v1/BETA/media/download",
        "method": "POST",
        "headers": {
          "x-api-key": "{{ $env.NCA_API_KEY }}"
        },
        "body": {
          "media_url": "={{ $input.first().json.urls[0] }}",
          "thumbnails": { "download": true },
          "cloud_upload": true
        }
      }
    },
    {
      "name": "Extract Thumbnail & Transcribe",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [1050, 300],
      "parameters": {
        "url": "http://localhost:8080/v1/media/transcribe",
        "method": "POST",
        "headers": {
          "x-api-key": "{{ $env.NCA_API_KEY }}"
        },
        "body": {
          "media_url": "={{ $input.prev(2).json.data.s3_url }}",
          "language": "vi"
        }
      }
    },
    {
      "name": "Add Vietnamese Captions",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [1250, 300],
      "parameters": {
        "url": "http://localhost:8080/v1/video/caption",
        "method": "POST",
        "headers": {
          "x-api-key": "{{ $env.NCA_API_KEY }}"
        },
        "body": {
          "video_url": "={{ $input.prev(2).json.data.s3_url }}",
          "transcript": "={{ $input.prev().json.transcript }}"
        }
      }
    },
    {
      "name": "Post to Facebook",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [1450, 300],
      "parameters": {
        "url": "http://localhost:5000/api/post/feed",
        "method": "POST",
        "body": {
          "profile": "my_account",
          "content": "={{ $input.first().json.summary }}",
          "media": "={{ $input.prev(1).json.data.s3_url }}"
        }
      }
    },
    {
      "name": "Check Success",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [1650, 300],
      "parameters": {
        "conditions": {
          "case1": {
            "condition": "string",
            "value1": "={{ $input.first().json.status }}",
            "operation": "equals",
            "value2": "success"
          }
        }
      }
    },
    {
      "name": "Success Notification",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1,
      "position": [1850, 200],
      "parameters": {
        "chatId": "{{ $env.TELEGRAM_CHAT_ID }}",
        "text": "✅ Đã đăng video lên Facebook thành công!"
      }
    },
    {
      "name": "Error Notification",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2,
      "position": [1850, 400],
      "parameters": {
        "toEmail": "{{ $env.ADMIN_EMAIL }}",
        "subject": "❌ Facebook Post Failed",
        "textContent": "={{ $input.first().json.error }}"
      }
    }
  ]
}
```

---

### **Tình Huống 2: Batch Posting Từ Google Sheets + AI Content Enhancement**

**Mục tiêu:**
- Đọc content từ Google Sheets
- Dùng AI để improve content (ngữ pháp, tone)
- Process media với NCA Toolkit
- Đăng lên multiple Facebook profiles

**Workflow:**
```
[Cron Trigger - Daily 10:00 AM]
    ↓
[Google Sheets]
    └─ Read: content, profile, image_urls
    ↓
[Loop through each row]
    │
    ├─ Row 1 (Profile A, Content A, Image A)
    │   ├─ Perplexity: Enhance content
    │   ├─ NCA: Process image (resize, optimize)
    │   └─ Flask: Post to Facebook
    │
    ├─ Row 2 (Profile B, Content B, Image B)
    │   ├─ Perplexity: Enhance content
    │   ├─ NCA: Process image
    │   └─ Flask: Post to Facebook
    │
    └─ [Continue for all rows]
    ↓
[Aggregate Results]
    ├─ Success count: 15/15
    ├─ Failed count: 0/15
    │
[Send Report Email]
    └─ HTML report with stats + screenshots
```

**Key Nodes:**

```
┌─ Google Sheets (Range: "Batch!A2:D100")
├─ For Each Item in List
│  ├─ Perplexity (Enhance Content)
│  │  └─ Prompt: "Sửa lỗi ngữ pháp, thêm emoji, giữ tone friendly"
│  │
│  ├─ NCA Toolkit (Image Processing)
│  │  ├─ POST /v1/image/convert/video (Image → Video with zoom)
│  │  └─ POST /v1/media/convert (Optimize format)
│  │
│  ├─ Flask API (Post to Facebook)
│  │  └─ POST /api/post/feed
│  │     Body: {profile, content, media}
│  │
│  └─ Error Handling
│     ├─ If Success: Mark "✅ Done" in Sheets
│     └─ If Error: Log to "Errors" Sheet + Email
│
└─ Send Summary Report
   ├─ Email with stats
   └─ Update Dashboard
```

---

### **Tình Huống 3: Tự Động Tạo Captions + Thumbnail Từ Kho Video**

**Mục tiêu:**
- Quét thư mục video  
- Auto-generate captions (NCA)
- Tạo thumbnail đẹp (AI + NCA)
- Upload to S3/Cloud

**Workflow:**
```
[Trigger: Folder Watch (hay Manual)]
    ↓
[List Files: /data/videos/*.mp4]
    ↓
[For Each Video File]
    │
    ├─ Extract Audio
    │  └─ NCA: /v1/media/convert/mp3
    │
    ├─ Transcribe + Translate
    │  └─ NCA: /v1/media/transcribe (vi)
    │
    ├─ Generate Captions
    │  ├─ Perplexity: Create catchy caption (khoa)
    │  └─ Content: "Tóm tắt video này thành 1 caption 1-2 dòng cho Facebook"
    │
    ├─ Create Thumbnail
    │  ├─ Extract best frame: /v1/video/thumbnail
    │  ├─ Perplexity: Generate thumbnail text
    │  └─ NCA: Add text overlay to image
    │
    ├─ Upload to S3
    │  └─ /v1/s3/upload
    │
    └─ Update Database
       └─ Store: video_id, captions, thumbnail_url
```

---

## 🔧 Cài Đặt & Cấu Hình

### **Step 1: Cài Đặt N8N**

```bash
# Option A: npm global
npm install -g n8n
n8n start

# Option B: Docker
docker run -it --rm \
  -p 5678:5678 \
  -e DB_TYPE=sqlite \
  -e DB_SQLITE_PATH=/data/n8n.db \
  -v ~/.n8n:/home/node/.n8n \
  -v /data:/data \
  n8nio/n8n

# Access: http://localhost:5678
```

### **Step 2: Cài Đặt NCA Toolkit**

```bash
# Option 1: Docker (Recommended)
docker pull n8nio/nca-toolkit:latest
docker run -p 8080:8080 \
  -e API_KEY=test123 \
  n8nio/nca-toolkit:latest

# Option 2: Local Installation
npm install -g nca-toolkit
nca-toolkit start --port 8080

# Test
curl http://localhost:8080/v1/toolkit/test
```

### **Step 3: Cấu Hình Environment Variables**

**File: `.env`**
```env
# --- N8N ---
N8N_PORT=5678
N8N_HOST=0.0.0.0

# --- NCA Toolkit ---
NCA_API_URL=http://localhost:8080
NCA_API_KEY=test123

# --- AI / Perplexity ---
PERPLEXITY_TOKEN=your_token_here
PERPLEXITY_MODEL=pplx-7b-online

# --- Facebook ---
FB_PROFILE_DIR=./data/profiles
FB_LOGS_DIR=./data/logs

# --- Flask API (Playwright Bridge) ---
FLASK_API_URL=http://localhost:5000
FLASK_API_PORT=5000

# --- Google Sheets ---
GOOGLE_SHEETS_API_KEY=your_key_here
GOOGLE_SHEETS_ID=your_sheet_id

# --- Notifications ---
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
ADMIN_EMAIL=your@email.com

# --- NCA Toolkit (S3/Cloud Upload) ---
S3_BUCKET=my-bucket
S3_REGION=us-east-1
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=yyy
```

### **Step 4: Thiết Lập Credentials trong N8N**

**N8N UI (http://localhost:5678):**

1. **Google Sheets:**
   - Click "Credentials" → New
   - Type: Google Sheets API
   - Upload service account JSON
   - Save

2. **Telegram:**
   - Type: Telegram Bot
   - Bot Token: từ BotFather
   - Save

3. **Gmail:**
   - Type: Gmail
   - OAuth2 setup
   - Save

4. **HTTP Headers (NCA Toolkit):**
   - Type: HTTP Custom Headers
   - Header: `x-api-key`
   - Value: `test123`

---

## 🎨 Các Nodes N8N Cần Thiết

### **Data Sources**
- **Cron**: Trigger theo lịch (mỗi ngày, mỗi giờ)
- **Webhook**: Trigger từ bên ngoài
- **Google Sheets**: Read/Write data
- **File System**: Read files

### **AI & Processing**
- **HTTP Request** (→ Perplexity API)
- **HTTP Request** (→ NCA Toolkit)
- **Code Node**: JavaScript/Python logic
- **Function Item**: Transform data

### **Facebook Automation**
- **HTTP Request** (→ Flask API)
  ```
  URL: http://localhost:5000/api/post/feed
  Method: POST
  Headers: Content-Type: application/json
  Body: {
    "profile": "my_account",
    "content": "...",
    "media": "..."
  }
  ```

### **Notifications**
- **Gmail**: Send email
- **Telegram**: Send messages
- **Slack**: Send to channel
- **SMS**: Via Twilio

### **Logic & Routing**
- **If**: Conditional branching
- **Switch**: Multiple conditions
- **Merge**: Combine data from multiple paths
- **Loop**: Process multiple items
- **Wait**: Delay execution

---

## 📝 API Endpoints Reference

### **Flask (Playwright Engine)**
```
POST http://localhost:5000/api/post/feed
POST http://localhost:5000/api/post/reel
GET  http://localhost:5000/api/profiles
GET  http://localhost:5000/api/logs?profile=xxx
```

### **NCA Toolkit**
```
POST http://localhost:8080/v1/BETA/media/download          # YouTube download
POST http://localhost:8080/v1/video/thumbnail              # Extract thumbnail
POST http://localhost:8080/v1/media/transcribe             # Transcribe/Translate
POST http://localhost:8080/v1/video/caption                # Add captions
POST http://localhost:8080/v1/media/convert                # Format conversion
POST http://localhost:8080/v1/s3/upload                    # S3 upload
GET  http://localhost:8080/v1/toolkit/test                 # Health check
```

### **Perplexity (via HTTP)**
```
POST http://localhost:8000/v1/chat/completions
Headers: Authorization: Bearer YOUR_TOKEN
Body: {
  "model": "pplx-7b-online",
  "messages": [{"role": "user", "content": "..."}]
}
```

---

## 🔐 Security Best Practices

### **1. API Keys & Secrets**

✅ **DO:**
```env
# Store in .env (git-ignored)
PERPLEXITY_TOKEN=secret_token_xyz
NCA_API_KEY=api_key_xyz
```

❌ **DON'T:**
```
# Don't hardcode in workflow JSON
{
  "api_key": "secret_xyz"  // ← EXPOSED in N8N UI
}
```

### **2. N8N Credentials Management**

- Use N8N's built-in Credentials system
- Store sensitive data in Vault (on-premise)
- Enable encryption at rest
- Rotate API keys regularly

### **3. Network Security**

```bash
# Run services in Docker network (isolated)
docker network create automation_net
docker run --network automation_net flask_api
docker run --network automation_net nca_toolkit
docker run --network automation_net n8n

# Access from N8N → http://flask_api:5000 (internal)
# Access from outside → http://localhost:5000 (external)
```

### **4. Rate Limiting & Throttling**

N8N config:
```bash
N8N_PERSONALIZATION_ENABLED=false
N8N_EXECUTION_TIMEOUT=600  # 10 minutes max
N8N_EXECUTION_DATA_PRUNE_TIMEOUT=3600  # 1 hour auto-cleanup
```

### **5. Webhook Security**

```json
{
  "trigger": "webhook",
  "options": {
    "httpMethod": "POST",
    "path": "long-random-path-xyz-123",
    "authentication": "basicAuth",
    "basicAuth": {
      "username": "admin",
      "password": "strong_password"
    }
  }
}
```

---

## ⚠️ Error Handling Patterns

### **Pattern 1: Try-Catch Email Notification**

```
[Main Flow]
    ↓
[Error Caught?] ← If any node fails
    ├─ YES → [Send Error Email]
    │        Body: Error message, Stack trace
    │
    └─ NO → [Send Success Notification]
            Body: Completed successfully
```

### **Pattern 2: Retry on Failure**

```json
{
  "node": "HTTP Request",
  "typeVersion": 4,
  "options": {
    "url": "http://localhost:5000/api/post/feed",
    "retry": {
      "maxTries": 3,
      "delay": 5000,
      "backoffMultiplier": 2
    }
  }
}
```

### **Pattern 3: Fallback Route**

```
[Primary Processing]
    ├─ Success → Continue
    ├─ Failure → Try Backup Service
    │           ├─ Success → Continue
    │           └─ Failure → Alert + Log
```

### **Pattern 4: Dead Letter Queue**

```
[Process Items]
    ├─ Item 1: Success ✅
    ├─ Item 2: Failure → Save to "errors.json"
    ├─ Item 3: Success ✅
    │
[End of Loop]
    ↓
[Any Errors?]
    ├─ YES → Email admin with failed items
    └─ NO  → Send success summary
```

---

## 📊 Monitoring & Logging

### **N8N Execution Logs**

Access: `http://localhost:5678` → Executions tab

**Track:**
- ✅ Successful runs
- ❌ Failed runs (with error details)
- ⏱️ Execution time
- 📊 Data flow (inputs/outputs)

### **Flask API Logs**

File: `data/logs/{profile}_log.json`

```json
[
  {
    "timestamp": "2024-03-27T09:30:00.123Z",
    "action": "post_feed",
    "profile": "my_account",
    "status": "success",
    "content": "...",
    "message": "Posted successfully"
  }
]
```

### **NCA Toolkit Logs**

```bash
# Docker logs
docker logs nca_toolkit_container

# Check job status
curl http://localhost:8080/v1/toolkit/jobs/status
```

### **Dashboard Monitoring**

Flask dashboard (`http://localhost:5000`):
- Real-time profile status
- Recent logs (last 50 entries)
- Posting stats
- Error alerts

---

## 🎯 Advanced Patterns

### **Pattern 1: AI Content Strategy Loop**

```
[Perplexity Analysis]
    └─ "Analyze top 10 Facebook trends today"
    
[Extract Topics]
    └─ Array: ["Topic A", "Topic B", "Topic C"]

[For Each Topic]
    ├─ Generate content (Perplexity)
    ├─ Find relevant image (Google Search → NCA Download)
    ├─ Create video (NCA)
    ├─ Add captions (NCA)
    └─ Post to Facebook (Flask API)

[Aggregate Results]
    └─ Report: 3 posts created, all successful
```

**N8N Nodes:**
1. Cron Trigger
2. HTTP → Perplexity (get trends)
3. Code (parse topics)
4. Loop → For each topic
   - HTTP → Perplexity (generate content)
   - HTTP → Google (find image)
   - HTTP → NCA (download + process)
   - HTTP → NCA (create video)
   - HTTP → NCA (add captions)
   - HTTP → Flask (post)
5. Email (send report)

---

### **Pattern 2: Multi-Channel Broadcasting**

```
[Prepare Content]
    ├─ Get from DB
    ├─ Process with NCA
    ├─ Enhance with AI

[Broadcast Strategy]
    ├─ Split A: Facebook (personal profiles)
    ├─ Split B: Facebook (business pages)
    ├─ Split C: Instagram (via graph API)
    ├─ Split D: Telegram (via bot)
    └─ Merge: Aggregate results

[Notification Strategy]
    ├─ Success → Telegram notification
    ├─ Partial → Email alert
    └─ Failure → SMS + Email + Slack
```

---

### **Pattern 3: Smart Scheduling Based on Analytics**

```
[Get Facebook Insights]
    └─ When do followers most active?
    
[Perplexity Analysis]
    └─ "When should I post based on my audience?"
    
[Schedule Dynamically]
    └─ Cron: 0 14 * * * (2:00 PM - best time)
    
[Post Content]
    └─ Optimal time = maximum reach
```

---

## 📋 Complete Example: Daily YouTube Content Curator

### **Workflow Overview**
Every day at 9 AM:
1. Perplexity finds top YouTube videos
2. NCA downloads + processes
3. Content enhanced with AI
4. Video posted to Facebook
5. Report emailed to admin

### **JSON Template**

```json
{
  "name": "Daily YouTube Curator → Facebook",
  "active": true,
  "nodes": [
    {
      "name": "Cron: 9 AM Daily",
      "type": "n8n-nodes-base.cron",
      "position": [250, 300],
      "parameters": {
        "cronExpression": "0 9 * * *",
        "timezone": "Asia/Ho_Chi_Minh"
      }
    },
    {
      "name": "Find Hot Videos",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300],
      "parameters": {
        "url": "http://localhost:8000/v1/chat/completions",
        "method": "POST",
        "headers": {
          "Authorization": "Bearer {{ $env.PERPLEXITY_TOKEN }}"
        },
        "body": {
          "model": "pplx-7b-online",
          "messages": [
            {
              "role": "user",
              "content": "Tìm top 5 video YouTube hot nhất hôm nay về [YOUR_TOPIC]. Trả URL + title + description"
            }
          ]
        }
      }
    },
    {
      "name": "Download + Process",
      "type": "n8n-nodes-base.httpRequest",
      "position": [650, 300],
      "parameters": {
        "url": "http://localhost:8080/v1/BETA/media/download",
        "method": "POST",
        "headers": {
          "x-api-key": "{{ $env.NCA_API_KEY }}"
        },
        "body": {
          "media_url": "={{ $input.first().json.urls[0] }}",
          "thumbnails": { "download": true },
          "cloud_upload": true
        }
      }
    },
    {
      "name": "Post to Facebook",
      "type": "n8n-nodes-base.httpRequest",
      "position": [850, 300],
      "parameters": {
        "url": "http://localhost:5000/api/post/feed",
        "method": "POST",
        "body": {
          "profile": "my_account",
          "content": "={{ $input.first().json.summary }}",
          "media": "={{ $input.prev().json.data.s3_url }}"
        }
      }
    },
    {
      "name": "Send Report",
      "type": "n8n-nodes-base.emailSend",
      "position": [1050, 300],
      "parameters": {
        "toEmail": "{{ $env.ADMIN_EMAIL }}",
        "subject": "✅ Daily Curator Report - {{ $now.format('YYYY-MM-DD') }}",
        "textContent": "YouTube video posted successfully to Facebook!"
      }
    }
  ],
  "connections": {
    "Cron: 9 AM Daily": [
      { "node": "Find Hot Videos", "type": "main", "index": 0 }
    ],
    "Find Hot Videos": [
      { "node": "Download + Process", "type": "main", "index": 0 }
    ],
    "Download + Process": [
      { "node": "Post to Facebook", "type": "main", "index": 0 }
    ],
    "Post to Facebook": [
      { "node": "Send Report", "type": "main", "index": 0 }
    ]
  }
}
```

---

## 🚨 Troubleshooting

### **N8N không kết nối tới NCA Toolkit**

```bash
# Check if NCA is running
curl http://localhost:8080/v1/toolkit/test

# If 404: start NCA
docker run -p 8080:8080 n8nio/nca-toolkit:latest

# Update N8N HTTP node URL to match
```

### **Flask API trả về 400 Bad Request**

```bash
# Check Flask logs
# data/logs/{profile}_log.json

# Verify payload format
{
  "profile": "correct_profile_name",  # ← Must be in data/profiles/
  "content": "text content",           # ← Not empty
  "media": "url_or_path"               # ← Valid file
}
```

### **Perplexity timeout sau 30s**

```json
{
  "wait": 60,  // Check N8N "Wait" node sau Perplexity call
  "retry": {
    "maxTries": 2,    // Retry once if timeout
    "delay": 5000
  }
}
```

### **S3 Upload fail**

```bash
# Verify AWS credentials
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=yyy

# Check bucket exists & has write permissions
aws s3 ls s3://my-bucket/
```

---

## 📈 Performance Tips

1. **Workflow Optimization:**
   - Use "Merge" node để combine parallel flows
   - Avoid unnecessary "Wait" nodes
   - Cache results khi possible

2. **Database Optimization:**
   - Prune old executions: `N8N_EXECUTION_DATA_PRUNE_TIMEOUT=3600`
   - Use SQLite (sufficient for most cases)

3. **Media Optimization:**
   - NCA hỗ trợ async: không cần wait full time
   - Compress images before uploading
   - Use WebP format cho web

4. **Parallel Processing:**
   - Process multiple profiles cùng lúc
   - Use N8N Queues for heavy workloads
   - Implement Rate Limiting

---

## ✅ Checklist: Setup Complete

- [ ] N8N running (`http://localhost:5678`)
- [ ] NCA Toolkit running (`http://localhost:8080`)
- [ ] Flask API running (`http://localhost:5000`)
- [ ] `.env` configured với keys
- [ ] Google Sheets credentials added
- [ ] Telegram/Email configured
- [ ] First workflow tested
- [ ] Facebook profiles validated
- [ ] Monitoring dashboard accessible
- [ ] Error alerts configured

---

## 🤝 Support & Next Steps

**Cần giúp?**
1. Check N8N logs: `http://localhost:5678` → Executions
2. Check Flask logs: `data/logs/`
3. Test endpoints: `curl http://localhost:8080/v1/toolkit/test`

**Tiếp theo:**
1. ✅ Tạo workflow đầu tiên (Start simple!)
2. ✅ Add more AI prompts cho nội dung
3. ✅ Integrate với CRM/Database
4. ✅ Scale to multiple profiles

---

**Hệ thống này cho phép bạn:**
- 🤖 Tự động hoá 100% quy trình Facebook
- 🧠 Sử dụng AI cho content strategy
- 🎬 Process media professional grade
- 📊 Monitor & optimize campaigns
- 🚀 Scale từ 1 tới 100 profiles

**Happy Automating! 🎉**
