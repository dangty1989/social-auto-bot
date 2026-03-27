"""
TY AUTOMATION - Động cơ Khách Hàng Facebook
Dùng Playwright để tự động đăng bài trên Facebook cá nhân
"""
import os, sys, time, random, argparse, json
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

PROFILES_DIR = os.environ.get("FB_PROFILES_DIR", os.path.join(ROOT_DIR, "data", "profiles"))
LOGS_DIR = os.environ.get("LOGS_DIR", os.path.join(ROOT_DIR, "data", "logs"))

os.makedirs(PROFILES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)


class FBClient:
    """Lớp quản lý tài khoản Facebook (đăng nhập, đăng bài)"""
    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.profile_dir = os.path.join(PROFILES_DIR, profile_name)
        self.log_file = os.path.join(LOGS_DIR, f"{profile_name}_log.json")
        os.makedirs(self.profile_dir, exist_ok=True)

    def _log(self, action, status, message=""):
        """Ghi nhật ký mỗi hành động vào file JSON"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "status": status,
            "message": message
        }
        logs = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
        logs.append(log_entry)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs[-100:], f, ensure_ascii=False, indent=2)  # Giới hạn 100 entries

    def _delay(self, min_sec=3, max_sec=7):
        """Chờ ngẫu nhiên giữa các hành động (giống con người)"""
        time.sleep(random.uniform(min_sec, max_sec))

    def _type_human(self, locator, text):
        """Gõ từng ký tự chậm (tránh phát hiện bot)"""
        if not text:
            return
        for char in text:
            locator.type(char, delay=random.uniform(50, 150))

    def login(self):
        print(f"\n{'='*60}")
        print(f"  DANG NHAP FACEBOOK - PROFILE: {self.profile_name}")
        print(f"{'='*60}")
        print("\n[*] Mo Chrome...")
        print("[*] Dang nhap vao Facebook...")
        print("[!] SAU KHI DANG NHAP XONG, HAY DONG TRINH DUYET")
        print("[!] Phien lam se duoc luu, khong can dang nhap lai\n")

        self._log("login", "started", "")

        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=self.profile_dir,
                channel="chrome",
                headless=False
            )
            page = ctx.new_page()
            try:
                page.goto("https://www.facebook.com/")
                page.wait_for_timeout(300000)
            except:
                pass
            finally:
                ctx.close()

        print("\n[OK] Da luu phien. Co the dong trinh duyet.\n")
        self._log("login", "success", "Session saved successfully")

    def post_feed(self, content, media_paths=None, private=True):
        print(f"\n{'='*60}")
        print(f"  DANG BAI FEED")
        print(f"{'='*60}")
        print(f"Noi dung: {content[:50]}...")
        print(f"Anh/video: {len(media_paths) if media_paths else 0} file")
        print(f"Che do: {'RIENG TU' if private else 'CONG KHAI'}")
        print(f"{'='*60}\n")

        self._log("post_feed", "started", content[:100])

        try:
            with sync_playwright() as p:
                ctx = p.chromium.launch_persistent_context(
                    user_data_dir=self.profile_dir,
                    channel="chrome",
                    headless=False,
                    viewport={"width": 1280, "height": 720}
                )
                page = ctx.new_page()

                page.goto("https://www.facebook.com/")
                self._delay(5, 8)
                page.keyboard.press("Escape")

                page.locator('div[role="button"]:has-text("on your mind"), div[role="button"]:has-text("dang nghi gi")').first.click()
                self._delay(4, 6)

                if private:
                    try:
                        aud = page.locator('div[role="button"] >> text=/Cong khai|Public|Ban be|Friends/').first
                        aud.click()
                        self._delay(3, 5)
                        page.locator('text=/Only me|Chi minh toi/').first.click()
                        self._delay(2, 4)
                    except:
                        pass

                if media_paths:
                    try:
                        page.set_input_files('input[type="file"]', media_paths)
                        self._delay(6, 10)
                    except Exception as e:
                        print(f"[!] Khong upload duoc media: {e}")

                tb = page.locator('div[role="textbox"][contenteditable="true"]').nth(-1)
                tb.focus()
                self._type_human(tb, content)
                self._delay(3, 5)

                btn = page.locator('div[role="button"]:has-text("Dang"), div[role="button"]:has-text("Post")').last
                btn.click()
                self._delay(10, 15)

                ctx.close()

            print("\n[OK] DANG BAI THANH CONG!\n")
            self._log("post_feed", "success", content[:100])
            return True

        except Exception as e:
            print(f"\n[!] LOI DANG BAI: {str(e)}\n")
            self._log("post_feed", "error", str(e))
            return False

    def post_reel(self, video_path, content, private=True):
        print(f"\n{'='*60}")
        print(f"  DANG REEL")
        print(f"{'='*60}")
        print(f"Video: {video_path}")
        print(f"Mo ta: {content[:50]}...")
        print(f"Che do: {'RIENG TU' if private else 'CONG KHAI'}")
        print(f"{'='*60}\n")

        self._log("post_reel", "started", f"{video_path} | {content[:50]}")

        try:
            with sync_playwright() as p:
                ctx = p.chromium.launch_persistent_context(
                    user_data_dir=self.profile_dir,
                    channel="chrome",
                    headless=False
                )
                page = ctx.new_page()

                page.goto("https://www.facebook.com/reels/create/")
                self._delay(8, 12)

                page.set_input_files('input[type="file"]', video_path)
                self._delay(10, 15)

                for _ in range(2):
                    page.locator('div[role="button"]:has-text("Next"), div[role="button"]:has-text("Tiep")').first.click()
                    self._delay(3, 5)

                if private:
                    try:
                        aud = page.locator('div[role="button"] >> text=/Cong khai|Public/').first
                        aud.click()
                        self._delay(3, 5)
                        page.locator('text=/Only me|Chi minh toi/').first.click()
                        self._delay(2, 4)
                    except:
                        pass

                tb = page.locator('div[role="textbox"]')
                tb.focus()
                self._type_human(tb, content)
                self._delay(2, 4)

                page.locator('div[role="button"]:has-text("Publish"), div[role="button"]:has-text("Dang")').first.click()
                self._delay(15, 20)

                ctx.close()

            print("\n[OK] DANG REEL THANH CONG!\n")
            self._log("post_reel", "success", f"{video_path}")
            return True

        except Exception as e:
            print(f"\n[!] LOI DANG REEL: {str(e)}\n")
            self._log("post_reel", "error", str(e))
            return False

    def get_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []


def main():
    parser = argparse.ArgumentParser(description="TY Automation - Facebook Client")
    parser.add_argument("command", choices=["login", "post_feed", "post_reel", "logs"],
                        help="Lenh can thuc hien")
    parser.add_argument("--profile", default="profile_1", help="Ten profile (default: profile_1)")
    parser.add_argument("--content", help="Noi dung bai/mo ta")
    parser.add_argument("--media", help="Path anh/video (multiple files cach boi dau phay)")
    parser.add_argument("--private", action="store_true", default=True, help="Rieng tu (default: True)")

    args = parser.parse_args()
    client = FBClient(args.profile)

    if args.command == "login":
        client.login()
    elif args.command == "post_feed":
        if not args.content:
            print("[!] Thieu --content")
            return
        media = args.media.split(",") if args.media else None
        client.post_feed(args.content, media, args.private)
    elif args.command == "post_reel":
        if not args.media or not args.content:
            print("[!] Thieu --media hoac --content")
            return
        client.post_reel(args.media, args.content, args.private)
    elif args.command == "logs":
        logs = client.get_logs()
        print(f"\n{'='*60}")
        print(f"  LOG - PROFILE: {args.profile}")
        print(f"{'='*60}\n")
        for log in logs[-20:]:
            print(f"[{log['timestamp']}] {log['action']} - {log['status']}")
            if log['message']:
                print(f"  └─ {log['message'][:60]}...")
        print()


if __name__ == "__main__":
    main()
