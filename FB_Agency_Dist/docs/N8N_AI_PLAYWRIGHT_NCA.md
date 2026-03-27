# 🚀 Hướng Dẫn Toàn Diện: n8n + AI + Playwright + NCA Toolkit

> **Mục tiêu:** Xây dựng hệ thống automation hoàn chỉnh — từ lên lịch nội dung đến đăng bài social media, tạo video, phân tích dữ liệu — không cần code phức tạp.

---

## 📐 Kiến Trúc Tổng Thể

```
┌─────────────────────────────────────────────────────────────────┐
│                    HỆ THỐNG AUTOMATION                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [TRIGGER]         [AI BRAIN]        [EXECUTOR]               │
│   n8n Workflow  →  Claude/GPT     →   Playwright               │
│   (Lên lịch)       (Viết nội dung)   (Đăng bài, Scrape)       │
│       │                                    │                   │
│       └──────►  NCA Toolkit  ◄─────────────┘                   │
│                 (Xử lý media)                                   │
│                                                                 │
│   ┌──────────────────────────────────────────────────┐         │
│   │              DATA FLOW                           │         │
│   │  Google Sheets → n8n → AI viết → Playwright đăng│         │
│   │  YouTube URL  → n8n → AI script → NCA video     │         │
│   │  Webhook      → n8n → AI phân tích → Telegram   │         │
│   └──────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### Các Thành Phần

| Thành phần | Vai trò | Port / URL |
|---|---|---|
| **n8n** | Điều phối workflow, lên lịch, kết nối các service | `localhost:5678` |
| **AI (Claude/GPT)** | Viết nội dung, phân tích, tạo script, quyết định | API qua HTTP |
| **Playwright** | Điều khiển browser: đăng bài, login, scrape | Flask API `localhost:5000` |
| **NCA Toolkit** | Xử lý media: cắt video, caption, download YouTube | `localhost:8080` |

---

## 🎯 4 Use Case Thực Tế

### Use Case 1: Social Media Auto-Post
```
Cron 8h sáng → Google Sheets lấy topic → Claude viết bài → 
Playwright đăng Facebook/Instagram → Telegram thông báo
```

### Use Case 2: YouTube → Short Video Pipeline
```
Telegram nhận link YouTube → NCA download + transcribe → 
AI viết script kịch bản → NCA cắt clip + thêm caption → 
NCA ghép video → Telegram gửi video hoàn chỉnh
```

### Use Case 3: Lead Generation + Phân Tích
```
Playwright scrape danh sách leads → AI phân loại và scoring → 
n8n lưu vào Supabase → Telegram báo cáo "top 10 leads hôm nay"
```

### Use Case 4: Báo Cáo Trang Web Tự Động
```
Cron hàng ngày → NCA screenshot các trang web → 
AI phân tích UI/UX → n8n tạo PDF báo cáo → Email gửi cho client
```

---

## ✅ Xác Nhận Từ Cộng Đồng (Nguồn: Internet 2024-2025)

> *Các thực tiễn sau được xác nhận bởi Tavily Web Search từ GitHub, Reddit, và n8n.io*

### n8n + Playwright — Cách Tốt Nhất

**Nguồn: Reddit r/n8n (2024):**
> *"Once the script was stable locally, I moved it to the server where my n8n instance runs. I just exposed the script as an API endpoint and triggered it from n8n using an HTTP Request node. This basically let me 'create' an API for a site that doesn't provide one."*

✅ **Kết luận xác nhận:** Luôn wrap Playwright trong Flask API → gọi qua HTTP Request node trong n8n.

### n8n + AI — Stack Thực Tế

**Nguồn: gadociconsulting.com (Social Media Engine):**
> *"The automation runs on n8n. Every hour, a scheduled workflow queries the Notion database for posts that are ready. It filters them by platform and sends each post to the appropriate social network."*

✅ **Kết luận:** Claude + Notion + n8n là stack được dùng phổ biến nhất cho social media automation.

### Async Polling — Pattern Chuẩn

**Nguồn: n8n.io/workflows/5447 (Advanced Retry):**
> *"Use a loop with Set, If, and Wait nodes for async job polling. Implement exponential backoff: delay_seconds × 2 mỗi lần retry."*

✅ **Kết luận:** Set node → Wait → HTTP Check → IF node → loop tối đa 5 lần với backoff.

### Playwright Anti-Detection — Kỹ Thuật 2025

**Nguồn: Bright Data + Scrapeless (2025):**
> *"Playwright Stealth plugin + disable navigator.webdriver + random mouse movements + keyboard delays là multi-faceted approach hiệu quả nhất."*

✅ **Kết luận:** `playwright-stealth` + persistent context + human-like delays.

---

## 🛠️ Cài Đặt Môi Trường

### Bước 1: Cài n8n

```bash
# Yêu cầu Node.js 18+ (tải tại nodejs.org)
npm install -g n8n

# Khởi động n8n
n8n start

# Truy cập: http://localhost:5678
```

**Docker (khuyến nghị cho production):**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=matkhau123 \
  n8nio/n8n
```

### Bước 2: Cài Playwright + Flask API

```bash
# Chạy SETUP.bat (Windows) - cài tất cả tự động
SETUP.bat

# Hoặc thủ công:
pip install playwright flask schedule python-dotenv playwright-stealth
playwright install chromium

# Khởi động Flask API
python app/dashboard.py
# Truy cập: http://localhost:5000
```

### Bước 3: Cài NCA Toolkit

```bash
# Tải bản NCA Toolkit từ repo
# Chạy local server
python nca_server.py  # hoặc theo hướng dẫn của NCA

# Kiểm tra: http://localhost:8080/v1/toolkit/test
```

### Bước 4: Chuẩn Bị AI API Key

Trong file `.env`:
```env
# Claude (Anthropic)
ANTHROPIC_API_KEY=sk-ant-...

# Hoặc OpenAI
OPENAI_API_KEY=sk-...

# Hoặc dùng qua OpenRouter (nhiều model)
OPENROUTER_API_KEY=sk-or-...
```

---

## 📊 Use Case 1: Social Media Auto-Post Chi Tiết

### Chuẩn Bị Google Sheets

Tạo Google Sheets với các cột:
| id | topic | profile | platform | schedule_time | status | post_id |
|---|---|---|---|---|---|---|
| 1 | Mẹo marketing | page_1 | facebook | 2026-01-15 08:00 | pending | |
| 2 | Tin tức AI | page_2 | facebook | 2026-01-15 10:00 | pending | |

### Workflow n8n: Social Auto-Post

#### Node 1 — Schedule Trigger
```json
{
  "nodeType": "n8n-nodes-base.cron",
  "name": "Chạy Mỗi Giờ",
  "parameters": {
    "triggerTimes": {
      "item": [{"mode": "everyHour"}]
    }
  }
}
```

#### Node 2 — Lấy Bài Chờ Đăng Từ Sheets
```json
{
  "nodeType": "n8n-nodes-base.googleSheets",
  "name": "Lấy Nội Dung",
  "parameters": {
    "operation": "getAll",
    "spreadsheetId": "YOUR_SHEET_ID",
    "range": "Sheet1",
    "filters": {
      "conditions": [
        {"field": "status", "value": "pending"},
        {"field": "schedule_time", "value": "={{ $now.format('yyyy-MM-dd HH:00') }}"}
      ]
    }
  }
}
```

#### Node 3 — AI Viết Nội Dung (Claude Sonnet)
```json
{
  "nodeType": "n8n-nodes-base.httpRequest",
  "name": "Claude Viết Bài",
  "parameters": {
    "method": "POST",
    "url": "https://api.anthropic.com/v1/messages",
    "headers": {
      "x-api-key": "={{ $env.ANTHROPIC_API_KEY }}",
      "anthropic-version": "2023-06-01",
      "content-type": "application/json"
    },
    "body": {
      "model": "claude-sonnet-4-5",
      "max_tokens": 500,
      "messages": [
        {
          "role": "user",
          "content": "Viết bài Facebook ngắn gọn, hấp dẫn về chủ đề: {{ $json.topic }}. Yêu cầu: 100-150 từ, thêm 3-5 emoji phù hợp, kết thúc bằng câu hỏi tương tác, thêm 3 hashtag tiếng Việt."
        }
      ]
    }
  }
}
```

**Parse kết quả AI trong Code Node:**
```javascript
// Node: Lấy Text Từ AI Response
const aiResponse = $input.first().json;
const content = aiResponse.content[0].text;

// Trả về nội dung sạch
return [{ json: { 
  content: content,
  profile: $('Lấy Nội Dung').first().json.profile,
  row_id: $('Lấy Nội Dung').first().json.id
}}];
```

#### Node 4 — Playwright Đăng Bài (Gọi Flask API)
```json
{
  "nodeType": "n8n-nodes-base.httpRequest",
  "name": "Đăng Facebook",
  "parameters": {
    "method": "POST",
    "url": "http://localhost:5000/api/post/feed",
    "body": {
      "profile": "={{ $json.profile }}",
      "content": "={{ $json.content }}"
    },
    "timeout": 60000
  }
}
```

**Điều phối nhiều profile cùng lúc (Loop Over Items):**
```json
{
  "nodeType": "n8n-nodes-base.splitInBatches",
  "name": "Đăng Lần Lượt",
  "parameters": {
    "batchSize": 1,
    "options": {"reset": false}
  }
}
```

#### Node 5 — Xử Lý Kết Quả
```javascript
// Code Node: Kiểm tra kết quả và chuẩn bị update Sheets
const result = $input.first().json;
const success = result.status === 'success';

return [{
  json: {
    row_id: $('Lấy Nội Dung').first().json.id, 
    status: success ? 'posted' : 'failed',
    posted_at: new Date().toISOString(),
    error: success ? '' : result.message
  }
}];
```

#### Node 6 — Cập Nhật Sheets + Thông Báo
```json
{
  "nodeType": "n8n-nodes-base.googleSheets",
  "name": "Đánh Dấu Đã Đăng",
  "parameters": {
    "operation": "update",
    "spreadsheetId": "YOUR_SHEET_ID",
    "range": "Sheet1",
    "filters": {"conditions": [{"field": "id", "value": "={{ $json.row_id }}"}]},
    "fieldsToUpdate": {
      "status": "={{ $json.status }}",
      "posted_at": "={{ $json.posted_at }}"
    }
  }
}
```

---

## 🎬 Use Case 2: YouTube → Short Video Pipeline

### Kiến Trúc Chi Tiết

```
Telegram Bot nhận link
    ↓
n8n Webhook nhận tin
    ↓
Node: NCA Download YouTube (lấy video + transcript)
    ↓
Node: AI phân tích → tạo scene list JSON
    ↓
Node: Loop → NCA cắt từng clip
    ↓
Node: NCA ghép video tất cả clip
    ↓
Node: NCA thêm caption
    ↓
Telegram gửi video
```

### Workflow Hoàn Chỉnh

#### Node 1 — Telegram Trigger
```json
{
  "nodeType": "n8n-nodes-base.telegramTrigger",
  "name": "Nhận Link YouTube",
  "parameters": {
    "updates": ["message"],
    "additionalFields": {}
  }
}
```

#### Node 2 — Validate URL (Code Node)
```javascript
const text = $input.first().json.message.text;
const youtubeRegex = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
const match = text.match(youtubeRegex);

if (!match) {
  throw new Error('Link không hợp lệ. Gửi link YouTube nhé!');
}

return [{ json: { 
  youtube_url: text.trim(),
  video_id: match[1],
  chat_id: $input.first().json.message.chat.id
}}];
```

#### Node 3 — NCA Download YouTube
```json
{
  "nodeType": "n8n-nodes-base.httpRequest",
  "name": "Download + Transcribe",
  "parameters": {
    "method": "POST",
    "url": "http://127.0.0.1:8080/v1/BETA/media/download",
    "headers": {"x-api-key": "test123"},
    "body": {
      "media_url": "={{ $json.youtube_url }}",
      "id": "={{ $json.video_id }}",
      "thumbnails": {"download": true},
      "cloud_upload": false
    }
  }
}
```

#### Node 4 — NCA Transcribe Video
```json
{
  "nodeType": "n8n-nodes-base.httpRequest",
  "name": "Lấy Transcript",
  "parameters": {
    "method": "POST",
    "url": "http://127.0.0.1:8080/v1/media/transcribe",
    "headers": {"x-api-key": "test123"},
    "body": {
      "media_url": "={{ $json.video_url }}",
      "language": "vi",
      "response_type": "segments"
    }
  }
}
```

#### Node 5 — AI Tạo Scene List
```json
{
  "nodeType": "n8n-nodes-base.httpRequest",  
  "name": "AI Viết Kịch Bản",
  "parameters": {
    "method": "POST",
    "url": "https://api.anthropic.com/v1/messages",
    "headers": {
      "x-api-key": "={{ $env.ANTHROPIC_API_KEY }}",
      "anthropic-version": "2023-06-01"
    },
    "body": {
      "model": "claude-sonnet-4-5",
      "max_tokens": 1000,
      "messages": [{
        "role": "user",
        "content": "Dựa vào transcript này, tạo SHORT VIDEO 60 giây.\n\nTranscript: {{ $json.segments }}\n\nYêu cầu: Chọn 5-7 đoạn hay nhất, mỗi đoạn 8-12 giây. Trả về JSON array:\n[{\"scene\": 1, \"start\": 10.5, \"end\": 22.0, \"caption\": \"text caption tiếng Việt\"}]\n\nCHỈ trả về JSON array thuần, không có text khác."
      }]
    }
  }
}
```

#### Node 6 — Parse Scene JSON (Code Node)
```javascript
const aiText = $input.first().json.content[0].text;

// Xử lý AI response có thể có markdown wrapper
let jsonText = aiText.trim();
if (jsonText.startsWith('```')) {
  jsonText = jsonText.replace(/```json?\n?/g, '').replace(/```$/g, '').trim();
}

const scenes = JSON.parse(jsonText);

// Chuẩn bị cho Loop
return scenes.map(scene => ({ json: {
  ...scene,
  video_url: $('Download + Transcribe').first().json.video_url,
  video_id: $('Nhận Link YouTube').first().json.video_id,
  chat_id: $('Nhận Link YouTube').first().json.chat_id
}}));
```

#### Node 7 — NCA Cắt Clip (trong Loop)
```json
{
  "nodeType": "n8n-nodes-base.httpRequest",
  "name": "Cắt Clip",
  "parameters": {
    "method": "POST",
    "url": "http://127.0.0.1:8080/v1/video/trim",
    "headers": {"x-api-key": "test123"},
    "body": {
      "video_url": "={{ $json.video_url }}",
      "start": "={{ $json.start }}",
      "end": "={{ $json.end }}",
      "id": "clip_={{ $json.video_id }}_={{ $json.scene }}"
    }
  }
}
```

#### Node 8 — Poll Job Status NCA (Code Node + Wait)
```javascript
// Dùng trong vòng lặp polling
const jobId = $input.first().json.job_id;
const maxRetry = 30;
let attempts = 0;

// Lưu job_id vào output để polling node kế tiếp dùng
return [{ json: { 
  job_id: jobId,
  clip_url: null, // sẽ được cập nhật sau khi poll
  scene: $input.first().json.scene
}}];
```

**Cách polling job NCA trong n8n (dùng Wait node):**
```
[HTTP Request: Cắt Clip]
    ↓
[Wait: 5 giây]  
    ↓  
[HTTP Request: GET /v1/toolkit/job/status?id={job_id}]
    ↓
[IF: status == "complete"]
    ├── YES → tiếp tục
    └── NO  → quay lại Wait (tối đa 10 lần)
```

#### Node 9 — Gộp Clip URLs + Ghép Video
```javascript
// Sau loop, gộp tất cả clip URLs
const clips = $input.all().map(item => item.json.output_url);
return [{ json: { clip_urls: clips }}];
```

```json
{
  "nodeType": "n8n-nodes-base.httpRequest",
  "name": "Ghép Video",
  "parameters": {
    "method": "POST",
    "url": "http://127.0.0.1:8080/v1/video/concatenate",
    "body": {
      "video_urls": "={{ $json.clip_urls }}",
      "id": "final_={{ $('Nhận Link YouTube').first().json.video_id }}"
    }
  }
}
```

#### Node 10 — NCA Thêm Caption
```json
{
  "nodeType": "n8n-nodes-base.httpRequest",
  "name": "Thêm Caption",
  "parameters": {
    "method": "POST",
    "url": "http://127.0.0.1:8080/v1/video/caption",
    "body": {
      "video_url": "={{ $json.final_video_url }}",
      "captions": "={{ $('AI Viết Kịch Bản').all().map(s => s.json.caption).join('|') }}",
      "style": "bottom_center",
      "font_size": 32
    }
  }
}
```

#### Node 11 — Telegram Gửi Video
```json
{
  "nodeType": "n8n-nodes-base.telegram",
  "name": "Gửi Video",
  "parameters": {
    "chatId": "={{ $('Nhận Link YouTube').first().json.chat_id }}",
    "operation": "sendVideo",
    "videoUrl": "={{ $json.captioned_video_url }}",
    "caption": "✅ Video đã xử lý xong!\n⏱️ {{ $json.duration }}s\n🎬 {{ $('AI Viết Kịch Bản').all().length }} cảnh"
  }
}
```

---

## 🔍 Use Case 3: Lead Generation Tự Động

### Playwright Scrape + AI Score

**Playwright (Flask API endpoint tùy chỉnh):**

Thêm vào `app/engine.py`:
```python
def scrape_leads(self, source_url: str) -> list:
    """Scrape danh sách leads từ URL nguồn."""
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            self.profile_dir,
            headless=True
        )
        page = browser.new_page()
        page.goto(source_url, wait_until='networkidle')
        
        leads = []
        items = page.query_selector_all('.lead-item, .contact-card, article')
        for item in items:
            lead = {
                'name': item.query_selector('.name, h2, h3').inner_text() if item.query_selector('.name, h2, h3') else '',
                'phone': item.query_selector('[class*=phone], [href^=tel]').inner_text() if item.query_selector('[class*=phone]') else '',
                'email': item.query_selector('[class*=email], [href^=mailto]').inner_text() if item.query_selector('[class*=email]') else '',
                'url': source_url
            }
            if lead['name']:
                leads.append(lead)
        
        browser.close()
        return leads
```

**n8n Workflow: Lead Pipeline**

```
[Cron hàng ngày 7h sáng]
    ↓
[HTTP: POST localhost:5000/api/scrape → Playwright scrape leads]
    ↓
[AI (Claude): Phân tích và cho điểm từng lead 0-100]
    ↓
[IF: score >= 70 → "Hot Lead"]
    ├── YES → Supabase insert + Telegram thông báo ngay
    └── NO  → Supabase insert (có thể theo dõi sau)
    ↓
[Tổng kết: Báo cáo cuối ngày qua Telegram]
```

**Code Node: AI Scoring**
```javascript
const leads = $input.all().map(item => item.json);

// Tạo prompt cho AI
const prompt = `Phân tích và chấm điểm các leads sau (0-100):

${JSON.stringify(leads, null, 2)}

Tiêu chí: 
- Có email: +30 điểm
- Có số điện thoại: +25 điểm  
- Tên đầy đủ: +15 điểm
- Website/mạng xã hội: +10 điểm
- Mô tả chi tiết: +20 điểm

Trả về JSON array: [{"name": "...", "score": 85, "reason": "có email + sdt + tên đầy đủ"}]
CHỈ trả về JSON, không có text khác.`;

// Gửi đến node AI tiếp theo
return [{ json: { leads, prompt }}];
```

---

## 📸 Use Case 4: Screenshot & Báo Cáo Tự Động

### n8n → NCA Screenshot → AI Phân Tích

#### Node 1 — Danh Sách URLs Cần Screenshot
```javascript
// Code Node: Định nghĩa URLs
const urlsToCapture = [
  { name: "Landing Page", url: "https://client.com", type: "marketing" },
  { name: "Dashboard", url: "https://app.client.com/dashboard", type: "app" },
  { name: "Competitor", url: "https://competitor.com", type: "research" }
];
return urlsToCapture.map(u => ({ json: u }));
```

#### Node 2 — NCA Chụp Screenshot
```json
{
  "nodeType": "n8n-nodes-base.httpRequest",
  "name": "Chụp Màn Hình",
  "parameters": {
    "method": "POST",
    "url": "http://127.0.0.1:8080/v1/image/screenshot/webpage",
    "body": {
      "url": "={{ $json.url }}",
      "full_page": true,
      "width": 1920,
      "height": 1080,
      "id": "screenshot_={{ $json.name.replace(' ', '_') }}"
    }
  }
}
```

#### Node 3 — AI Phân Tích Ảnh (Vision)
```json
{
  "nodeType": "n8n-nodes-base.httpRequest",
  "name": "AI Phân Tích UI",
  "parameters": {
    "method": "POST",
    "url": "https://api.anthropic.com/v1/messages",
    "body": {
      "model": "claude-opus-4-5",
      "max_tokens": 500,
      "messages": [{
        "role": "user",
        "content": [
          {
            "type": "image",
            "source": {
              "type": "url",
              "url": "={{ $json.screenshot_url }}"
            }
          },
          {
            "type": "text",
            "text": "Phân tích UI/UX trang web này. Đánh giá:\n1. Điểm mạnh (2-3 điểm)\n2. Điểm cần cải thiện (2-3 điểm)\n3. Điểm số tổng: 1-10\n4. Hành động ưu tiên nhất\nTrả lời ngắn gọn bằng tiếng Việt."
          }
        ]
      }]
    }
  }
}
```

---

## ⚙️ Tối Ưu AI Trong n8n

### Chọn Model Phù Hợp

| Task | Model Khuyến Nghị | Lý Do |
|---|---|---|
| Viết bài Facebook | `claude-haiku-3-5` | Nhanh, rẻ, đủ chất lượng |
| Phân tích video dài | `claude-sonnet-4-5` | Cân bằng tốt |
| Phân tích ảnh (Vision) | `claude-opus-4-5` hoặc `gpt-4o` | Chất lượng vision tốt |
| Scoring leads batch | `gpt-4o-mini` | Rẻ nhất cho batch |
| Script video phức tạp | `claude-sonnet-4-5` | Sáng tạo cao |

### Prompt Engineering Cho Automation

**Template Prompt Tốt:**
```
CONTEXT: [Mô tả ngắn về hệ thống]
TASK: [Yêu cầu cụ thể]
INPUT: [Dữ liệu đầu vào]
OUTPUT FORMAT: [Mô tả format JSON cụ thể]
CONSTRAINT: Chỉ trả về JSON, không có text thừa, không wrap trong markdown.
```

**Ví dụ thực tế:**
```
CONTEXT: Hệ thống tự động đăng bài Facebook cho agency marketing Việt Nam.
TASK: Viết bài Facebook hấp dẫn từ topic cho trước.
INPUT: Topic = "{{ $json.topic }}", Target audience = "{{ $json.audience }}"
OUTPUT FORMAT: {"content": "nội dung bài...", "hashtags": ["#tag1", "#tag2", "#tag3"]}
CONSTRAINT: Chỉ trả về JSON, không markdown wrapper.
```

### Xử Lý Lỗi AI Response

```javascript
// Code Node: Safe Parse AI Response
function safeParseAI(text) {
  try {
    // Thử parse trực tiếp
    return JSON.parse(text);
  } catch(e1) {
    // Thử remove markdown wrapper
    const cleaned = text
      .replace(/```json\n?/g, '')
      .replace(/```\n?/g, '')
      .trim();
    try {
      return JSON.parse(cleaned);
    } catch(e2) {
      // Extract JSON với regex
      const match = cleaned.match(/\{[\s\S]*\}|\[[\s\S]*\]/);
      if (match) return JSON.parse(match[0]);
      throw new Error('Không parse được AI response: ' + text.substring(0, 100));
    }
  }
}

const aiText = $input.first().json.content[0].text;
const parsed = safeParseAI(aiText);
return [{ json: parsed }];
```

---

## 🔒 Bảo Mật Hệ Thống

### 1. Environment Variables trong n8n

Không hardcode API keys trong workflow. Dùng n8n Credentials:

```
n8n Settings → Credentials → New:
- Anthropic Claude API Key
- OpenAI API Key  
- Telegram Bot Token
- Google Sheets OAuth
```

Tham chiếu trong node:
```
{{ $credentials.anthropicApi.apiKey }}
```

### 2. Bảo Vệ Flask API

Thêm API key authentication vào `app/dashboard.py`:
```python
import hashlib
import hmac

API_SECRET = os.getenv('FLASK_API_SECRET', 'changeme-in-production')

def require_api_key(f):
    """Decorator bảo vệ endpoint bằng API key."""
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key', '')
        if not hmac.compare_digest(key, API_SECRET):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

# Áp dụng cho tất cả API routes:
@app.route('/api/post/feed', methods=['POST'])
@require_api_key
def post_feed():
    ...
```

Trong n8n HTTP Request node:
```
Headers → Add Header:
  Name: X-API-Key
  Value: {{ $env.FLASK_API_SECRET }}
```

### 3. Rate Limiting Playwright

```python
# Trong app/engine.py - thêm rate limit giữa các post
import time
import random

class RateLimit:
    def __init__(self):
        self.last_action = {}
    
    def wait(self, profile_name):
        """Đảm bảo ít nhất 30-60 giây giữa 2 lần đăng cùng profile."""
        now = time.time()
        last = self.last_action.get(profile_name, 0)
        delay = random.uniform(30, 60)  # seconds
        
        if now - last < delay:
            wait_time = delay - (now - last)
            time.sleep(wait_time)
        
        self.last_action[profile_name] = time.time()

rate_limiter = RateLimit()
```

---

## 🔄 Pattern: Polling NCA Async Jobs

> **Nguồn xác nhận:** n8n.io/workflows/5447 — "Advanced retry and delay logic"

NCA Toolkit xử lý video bất đồng bộ (async). Pattern chuẩn từ cộng đồng n8n:

### Pattern Được Xác Nhận (Exponential Backoff)

```
[POST /v1/video/trim] → { job_id: "abc123" }
    ↓
[Set Node: attempt=0, delay=3]
    ↓
[Loop bắt đầu]
    ↓
[Wait: {{ $json.delay }} giây]           ← exponential backoff
    ↓
[GET /v1/toolkit/job/status?id=abc123]
    ↓
[IF: status == "complete"]
    ├── YES → Lấy output_url → Tiếp tục
    └── NO  → [IF: attempt < 5]
                   ├── YES → [Set: attempt=attempt+1, delay=delay*2] → Loop
                   └── NO (timeout) → Telegram cảnh báo
```

**Chú ý cộng đồng:** "Checking too frequently creates noise. Start with 5-second intervals for fast jobs (NCA video), 30-second for slow jobs."

### Pattern Trong n8n

```
[POST /v1/video/trim] → { job_id: "abc123" }
    ↓
[Code Node: Lưu job_id]
    ↓
[Loop bắt đầu]
    ↓
[Wait: 3 giây]
    ↓
[GET /v1/toolkit/job/status?id=abc123] → { status: "processing"|"complete"|"error" }
    ↓
[IF: status == "complete"]
    ├── YES → Lấy output_url → Tiếp tục workflow
    └── NO  → [IF: attempts < 20] → Quay lại Wait
                   └── NO (timeout) → Báo lỗi Telegram
```

**Code Node: Poll Manager**
```javascript
// Khởi tạo poll state
const jobId = $input.first().json.job_id;
const maxAttempts = 20;
const currentAttempt = parseInt($node["Poll Manager"].context?.attempt || "0") + 1;

if (currentAttempt > maxAttempts) {
  throw new Error(`Job ${jobId} timeout sau ${maxAttempts} lần thử`);
}

return [{ json: { 
  job_id: jobId,
  attempt: currentAttempt
}}];
```

---

## 📱 Tích Hợp Thông Báo Telegram

### Bot Telegram Cho Mọi Workflow

#### Tạo Telegram Bot
1. Nhắn `/newbot` cho **@BotFather** trên Telegram
2. Đặt tên bot
3. Nhận `BOT_TOKEN`
4. Lấy `CHAT_ID` bằng cách nhắn bot rồi truy cập: `https://api.telegram.org/bot{TOKEN}/getUpdates`

#### n8n Credentials
```
Type: Telegram API
Token: YOUR_BOT_TOKEN
```

#### Templates Thông Báo

**Đăng bài thành công:**
```
✅ Đã đăng bài thành công!
👤 Profile: {{ $json.profile }}
📝 Nội dung: {{ $json.content.substring(0, 80) }}...
🕐 Lúc: {{ $now.format('HH:mm dd/MM/yyyy') }}
```

**Lỗi hệ thống:**
```
❌ LỖI HỆ THỐNG
🔴 Module: {{ $json.module }}
📋 Lỗi: {{ $json.error }}
🕐 Lúc: {{ $now.format('HH:mm dd/MM/yyyy') }}
⚠️ Cần kiểm tra thủ công!
```

**Báo cáo cuối ngày:**
```
📊 BÁO CÁO NGÀY {{ $now.format('dd/MM/yyyy') }}

✅ Đã đăng: {{ $json.posted }} bài
❌ Thất bại: {{ $json.failed }} bài
🎬 Video tạo: {{ $json.videos }} clip
📸 Screenshot: {{ $json.screenshots }} ảnh

💰 Token AI đã dùng: {{ $json.tokens }}
```

---

## 🗂️ Cấu Trúc Dự Án Hoàn Chỉnh

```
project/
├── app/                         # Playwright + Flask API
│   ├── engine.py               # FBClient - automation engine
│   ├── dashboard.py            # Flask web + API endpoints
│   ├── scheduler.py            # Job scheduler
│   └── report.py               # Report generator
│
├── n8n-workflows/              # Export JSON workflows từ n8n
│   ├── social_autopost.json   # Use case 1: Social media
│   ├── youtube_pipeline.json  # Use case 2: Video pipeline
│   ├── lead_generation.json   # Use case 3: Leads
│   └── screenshot_report.json # Use case 4: Báo cáo
│
├── docs/                       
│   ├── N8N_AI_PLAYWRIGHT_NCA.md  # File này
│   └── N8N_INTEGRATION.md        # Hướng dẫn cơ bản
│
├── data/                       # Runtime data (gitignored)
│   ├── profiles/              # Chrome profiles
│   ├── logs/                  # JSON logs
│   ├── reports/               # HTML reports
│   └── schedules/             # Job queue
│
├── .env                        # API keys (gitignored)
├── .env.example               # Template .env
├── requirements.txt           # Python dependencies
├── SETUP.bat                  # One-click setup Windows
└── DASHBOARD.bat              # Launch web dashboard
```

---

## 🚦 Checklist Trước Khi Chạy

### Kiểm Tra Môi Trường
```bash
# 1. n8n đang chạy?
curl http://localhost:5678/healthz

# 2. Flask API đang chạy?
curl http://localhost:5000/api/profiles

# 3. NCA Toolkit đang chạy?
curl http://localhost:8080/v1/toolkit/test

# 4. AI API key hợp lệ?
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"claude-haiku-3-5","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
```

### Verify Script
```python
# python verify_all.py
import requests, json

checks = [
    ("n8n", "http://localhost:5678/healthz"),
    ("Flask", "http://localhost:5000/api/profiles"), 
    ("NCA", "http://localhost:8080/v1/toolkit/test"),
]

for name, url in checks:
    try:
        r = requests.get(url, timeout=5)
        status = "✅ OK" if r.status_code in [200, 201] else f"⚠️ HTTP {r.status_code}"
    except Exception as e:
        status = f"❌ Không kết nối được: {e}"
    print(f"{name:10} {status}")
```

---

## 💡 Mẹo & Tricks

### 1. Debug Workflow n8n
- Bật **"Execute Workflow"** trên từng node để test riêng lẻ
- Dùng **"PIN data"** để giữ output cũ khi test node kế tiếp
- Tab **"Output"** trên mỗi node hiển thị JSON output

### 2. Tối Ưu Chi Phí AI
```javascript
// Ưu tiên model rẻ cho tasks đơn giản
const model = contentLength > 3000 
  ? 'claude-sonnet-4-5'    // Complex: ~$3/1M tokens
  : 'claude-haiku-3-5';    // Simple: ~$0.25/1M tokens

// Cache kết quả AI (giảm 70% chi phí lặp lại)
// Dùng Supabase/Redis làm cache layer
```

### 3. Playwright Anti-Detection (2025 Best Practices)

> **Nguồn:** Bright Data + Scrapeless + Reddit r/automation (2025):  
> *"Multi-faceted approach: stealth plugin + navigator.webdriver override + random delays"*

```python
# engine.py - Multi-layer anti-detection
from playwright_stealth import stealth_sync
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
]

def _create_stealth_page(self, context):
    """Tạo page với full anti-detection theo best practices 2025."""
    page = context.new_page()
    
    # 1. Playwright-stealth: vô hiệu hóa navigator.webdriver
    stealth_sync(page)
    
    # 2. Override thêm các fingerprint
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        Object.defineProperty(navigator, 'languages', { get: () => ['vi-VN', 'vi', 'en-US'] });
    """)
    
    # 3. Random viewport (không phải fixed 1920x1080)
    page.set_viewport_size({
        'width': random.randint(1280, 1920),
        'height': random.randint(768, 1080)
    })
    
    return page
```

### 4. Retry Logic Trong n8n
```json
{
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 5000,
  "continueOnFail": false
}
```

### 5. Queue Content Thông Minh
```sql
-- Supabase table cho content queue
CREATE TABLE content_queue (
  id SERIAL PRIMARY KEY,
  platform VARCHAR(20),  -- facebook, instagram
  profile_name VARCHAR(50),
  content TEXT,
  media_url TEXT,
  scheduled_at TIMESTAMPTZ,
  status VARCHAR(20) DEFAULT 'pending',  -- pending, posted, failed
  retry_count INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 📚 Tổng Kết

| Thành phần | Chức năng chính | Khi nào dùng |
|---|---|---|
| **n8n** | Điều phối, lên lịch, kết nối | Luôn luôn — trung tâm workflow |
| **Claude/GPT** | Viết nội dung, phân tích, quyết định | Khi cần intelligence |
| **Playwright** | Login, đăng bài, scrape web | Khi cần browser automation |
| **NCA Toolkit** | Cắt video, caption, download, screenshot | Khi cần xử lý media |

**Luồng điển hình:**
```
n8n lên lịch → n8n gọi AI → AI viết nội dung
    → n8n gọi Playwright → Đăng lên mạng xã hội
    → n8n gọi NCA → Tạo video kèm theo
    → n8n gửi Telegram → Báo cáo cho bạn
```

> **Bắt đầu nhỏ:** Làm Use Case 1 (Social Auto-Post) trước, sau khi hoạt động ổn định mới thêm Use Case 2, 3, 4.

---

*Cập nhật: 2026-03-27 | Phiên bản: 1.1 | Nguồn tham khảo: Tavily Web Search (Reddit, n8n.io, GitHub, Bright Data, LinkedIn)*
