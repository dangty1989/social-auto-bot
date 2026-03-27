"""
TY AUTOMATION - Job Scheduler
Dat lich dang bai tu dong (1 lan, hang ngay, hang tuan)
"""
import os, sys, json, time, schedule, threading
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
load_dotenv(os.path.join(ROOT_DIR, ".env"))

from app.engine import FBClient

SCHEDULES_DIR = os.environ.get("SCHEDULES_DIR", os.path.join(ROOT_DIR, "data", "schedules"))
os.makedirs(SCHEDULES_DIR, exist_ok=True)


class FBScheduler:
    def __init__(self):
        self.jobs = []
        self.load_jobs()

    def load_jobs(self):
        jobs_file = os.path.join(SCHEDULES_DIR, "jobs.json")
        if os.path.exists(jobs_file):
            try:
                with open(jobs_file, 'r', encoding='utf-8') as f:
                    self.jobs = json.load(f)
            except:
                self.jobs = []

    def save_jobs(self):
        jobs_file = os.path.join(SCHEDULES_DIR, "jobs.json")
        with open(jobs_file, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, ensure_ascii=False, indent=2)

    def add_job(self, job_type, profile, time_str, content, media=None, repeat="once", private=True):
        job = {
            "id": int(time.time()),
            "type": job_type,
            "profile": profile,
            "time": time_str,
            "content": content,
            "media": media,
            "repeat": repeat,
            "private": private,
            "created": datetime.now().isoformat(),
            "next_run": None,
            "last_run": None,
            "status": "active",
            "run_count": 0
        }
        self.jobs.append(job)
        self.save_jobs()
        print(f"[+] Job {job['id']} added: {job_type} tai {time_str}")
        return job

    def remove_job(self, job_id):
        self.jobs = [j for j in self.jobs if j["id"] != job_id]
        self.save_jobs()
        print(f"[-] Job {job_id} removed")

    def pause_job(self, job_id):
        for job in self.jobs:
            if job["id"] == job_id:
                job["status"] = "paused"
                break
        self.save_jobs()

    def resume_job(self, job_id):
        for job in self.jobs:
            if job["id"] == job_id:
                job["status"] = "active"
                break
        self.save_jobs()

    def get_jobs(self):
        return self.jobs

    def execute_job(self, job):
        if job["status"] != "active":
            return
        print(f"\n{'='*60}")
        print(f"[*] RUNNING JOB: {job['id']} - {job['type']}")
        print(f"{'='*60}\n")
        try:
            client = FBClient(job["profile"])
            if job["type"] == "feed":
                media = job.get("media", [])
                if isinstance(media, str):
                    media = [media] if media else None
                client.post_feed(job["content"], media, job.get("private", True))
            elif job["type"] == "reel":
                client.post_reel(job["media"], job["content"], job.get("private", True))
            job["last_run"] = datetime.now().isoformat()
            job["run_count"] = job.get("run_count", 0) + 1
            print(f"\n[OK] Job {job['id']} executed successfully\n")
        except Exception as e:
            print(f"\n[!] Job {job['id']} error: {e}\n")
        finally:
            self.save_jobs()

    def start(self):
        print("\n" + "="*60)
        print("  TY AUTOMATION - JOB SCHEDULER")
        print("="*60)
        print(f"\n[*] Loaded {len(self.jobs)} jobs\n")

        scheduled_times = set()
        for job in self.jobs:
            if job["status"] != "active":
                continue
            time_str = job["time"]
            if job["repeat"] == "once":
                schedule.at(time_str).do(self.execute_job, job)
                scheduled_times.add(time_str)
                print(f"[*] {job['id']:12} | {job['type']:6} | {time_str} (once)")
            elif job["repeat"] == "daily":
                schedule.every().day.at(time_str).do(self.execute_job, job)
                scheduled_times.add(time_str)
                print(f"[*] {job['id']:12} | {job['type']:6} | {time_str} (daily)")
            elif job["repeat"] == "weekly":
                day = job.get("day", "monday")
                schedule.every().week.at(time_str, day).do(self.execute_job, job)
                scheduled_times.add(time_str)
                print(f"[*] {job['id']:12} | {job['type']:6} | {time_str} ({day})")

        print(f"\n[OK] Scheduler started. Runs at {sorted(scheduled_times)}")
        print("[!] Ctrl+C de dung\n")

        while True:
            try:
                schedule.run_pending()
                time.sleep(30)
            except KeyboardInterrupt:
                print("\n[*] Scheduler stopped\n")
                break
            except Exception as e:
                print(f"[!] Scheduler error: {e}")
                time.sleep(60)


# ============================================================
# CLI
# ============================================================

def show_menu():
    print("\n" + "="*60)
    print("  TY AUTOMATION - SCHEDULER MANAGER")
    print("="*60)
    print("\n[1] Them lich dang bai")
    print("[2] Xem danh sach")
    print("[3] Tam dung / Tiep tuc")
    print("[4] Xoa lich")
    print("[5] Chay scheduler")
    print("[0] Thoat\n")

def add_job_interactive(scheduler):
    print("\n--- THEM LICH DANG BAI ---")
    print("\nLoai (feed/reel):")
    job_type = input("> ").strip().lower()
    if job_type not in ["feed", "reel"]:
        print("Loai khong hop le")
        return
    print("\nTen profile (vd: profile_1):")
    profile = input("> ").strip()
    print("\nGio dang (HH:MM, vd: 14:30):")
    time_str = input("> ").strip()
    print("\nNoi dung:")
    content = input("> ").strip()
    print("\nDuong dan media (bo trong neu khong co):")
    media = input("> ").strip() or None
    print("\nLap lai (once/daily/weekly):")
    repeat = input("> ").strip().lower()
    if repeat not in ["once", "daily", "weekly"]:
        repeat = "daily"
    print("\nRieng tu (y/n, mac dinh: y):")
    private = input("> ").strip().lower() != "n"
    scheduler.add_job(job_type, profile, time_str, content, media, repeat, private)
    print("[OK] Da them lich!")

def list_jobs(scheduler):
    jobs = scheduler.get_jobs()
    if not jobs:
        print("\nChua co lich nao\n")
        return
    print("\n" + "="*100)
    print(f"{'ID':<12} {'Loai':<6} {'Profile':<12} {'Gio':<6} {'Lap lai':<8} {'Trang thai':<8} {'Lan':<5}")
    print("="*100)
    for j in jobs:
        print(f"{j['id']:<12} {j['type']:<6} {j['profile']:<12} {j['time']:<6} {j['repeat']:<8} {j['status']:<8} {j['run_count']:<5}")
    print("="*100 + "\n")

def pause_resume_job(scheduler):
    list_jobs(scheduler)
    print("Nhap Job ID:")
    try:
        job_id = int(input("> ").strip())
        job = next((j for j in scheduler.get_jobs() if j['id'] == job_id), None)
        if not job:
            print("Khong tim thay job")
            return
        if job['status'] == 'active':
            scheduler.pause_job(job_id)
            print("[OK] Da tam dung")
        else:
            scheduler.resume_job(job_id)
            print("[OK] Da tiep tuc")
    except:
        print("ID khong hop le")

def remove_job(scheduler):
    list_jobs(scheduler)
    print("Nhap Job ID de xoa:")
    try:
        job_id = int(input("> ").strip())
        scheduler.remove_job(job_id)
        print("[OK] Da xoa")
    except:
        print("ID khong hop le")


def main():
    scheduler = FBScheduler()
    while True:
        show_menu()
        choice = input("Chon: ").strip()
        if choice == "1":
            add_job_interactive(scheduler)
        elif choice == "2":
            list_jobs(scheduler)
        elif choice == "3":
            pause_resume_job(scheduler)
        elif choice == "4":
            remove_job(scheduler)
        elif choice == "5":
            scheduler.start()
        elif choice == "0":
            print("\nTam biet!\n")
            break
        else:
            print("Lua chon khong hop le")


if __name__ == "__main__":
    main()
