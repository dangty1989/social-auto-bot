# TY AUTOMATION - Facebook Auto Post

He thong tu dong dang bai len Facebook ca nhan.


## BAT DAU NHANH

### Lan dau tien
1. Double-click **SETUP.bat** (cho 5-10 phut de cai dat)
2. Double-click **DASHBOARD.bat** de mo giao dien

### Hang ngay
- Double-click **DASHBOARD.bat** -> Mo trinh duyet -> Dang bai


## CAU TRUC THU MUC

```
FB_Agency_Dist/
├── SETUP.bat          <- Cai dat (chay 1 lan)
├── DASHBOARD.bat      <- Mo giao dien (chay hang ngay)
├── README.md          <- File nay
├── .env.example       <- Mau cau hinh
├── requirements.txt   <- Thu vien Python
│
├── app/               <- Code (KHONG CAN MO)
│   ├── engine.py      <- Core Facebook automation
│   ├── dashboard.py   <- Web UI
│   ├── scheduler.py   <- Hen gio dang bai
│   ├── report.py      <- Bao cao hang ngay
│   ├── verify.py      <- Kiem tra he thong
│   └── templates/     <- Giao dien HTML
│
├── docs/              <- Tai lieu them (tuy chon)
│
└── data/              <- Du lieu (TU DONG TAO)
    ├── profiles/      <- Phien dang nhap Facebook
    ├── logs/          <- Lich su hoat dong
    ├── reports/       <- Bao cao HTML
    └── schedules/     <- Lich hen gio
```


## TINH NANG

- **Dang bai Feed**: Text + anh/video
- **Dang Reel**: Video ngan
- **Hen gio**: Tu dong dang theo lich (1 lan / hang ngay / hang tuan)
- **Bao cao**: Thong ke hoat dong hang ngay (HTML + email)
- **Da profile**: Quan ly nhieu tai khoan Facebook


## SU DUNG NANG CAO (CLI)

```bash
# Dang nhap Facebook
python app/engine.py login --profile profile_1

# Dang bai feed
python app/engine.py post_feed --profile profile_1 --content "Noi dung bai viet"

# Dang reel
python app/engine.py post_reel --profile profile_1 --media video.mp4 --content "Mo ta"

# Quan ly lich hen gio
python app/scheduler.py

# Tao bao cao
python app/report.py

# Kiem tra he thong
python app/verify.py
```


## CAU HINH

Sao chep `.env.example` thanh `.env` va sua cac gia tri:

| Bien              | Mo ta                    | Mac dinh         |
|-------------------|--------------------------|------------------|
| FB_PROFILES_DIR   | Thu muc luu profile      | ./data/profiles  |
| LOGS_DIR          | Thu muc logs             | ./data/logs      |
| REPORTS_DIR       | Thu muc bao cao          | ./data/reports   |
| SCHEDULES_DIR     | Thu muc lich hen         | ./data/schedules |
| FLASK_PORT        | Cong web dashboard       | 5000             |
| FLASK_HOST        | Host dashboard           | 127.0.0.1        |


## XU LY LOI

| Van de                    | Cach xu ly                              |
|---------------------------|-----------------------------------------|
| SETUP.bat bao loi Python  | Cai Python 3.8+ va tick "Add to PATH"   |
| Dashboard khong mo        | Kiem tra port 5000, chay lai DASHBOARD.bat |
| Dang bai that bai         | Dang nhap lai Facebook (Dang nhap button) |
| Chrome khong mo           | Chay `playwright install chromium`       |

Chay `python app/verify.py` de kiem tra toan bo he thong.
