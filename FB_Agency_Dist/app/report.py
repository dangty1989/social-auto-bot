"""
TY AUTOMATION - Daily Report Generator
Tao bao cao hoat dong hang ngay (HTML + email)
"""
import os, sys, json, smtplib
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

LOGS_DIR = os.environ.get("LOGS_DIR", os.path.join(ROOT_DIR, "data", "logs"))
REPORTS_DIR = os.environ.get("REPORTS_DIR", os.path.join(ROOT_DIR, "data", "reports"))
os.makedirs(REPORTS_DIR, exist_ok=True)


class ReportGenerator:
    def __init__(self):
        self.today = datetime.now().date()

    def get_todays_logs(self, profile):
        log_file = os.path.join(LOGS_DIR, f"{profile}_log.json")
        if not os.path.exists(log_file):
            return []
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_logs = json.load(f)
        except:
            return []
        today_logs = []
        for log in all_logs:
            try:
                log_date = datetime.fromisoformat(log['timestamp']).date()
                if log_date == self.today:
                    today_logs.append(log)
            except:
                pass
        return today_logs

    def get_all_profiles(self):
        profiles = []
        if os.path.exists(LOGS_DIR):
            for f in os.listdir(LOGS_DIR):
                if f.endswith("_log.json"):
                    profiles.append(f.replace("_log.json", ""))
        return sorted(profiles)

    def generate_html_report(self):
        profiles = self.get_all_profiles()
        report_data = {}
        total_posts = 0
        total_success = 0
        total_errors = 0

        for profile in profiles:
            logs = self.get_todays_logs(profile)
            stats = {
                "total": len(logs),
                "success": len([l for l in logs if l.get('status') == 'success']),
                "error": len([l for l in logs if l.get('status') == 'error']),
                "logs": logs
            }
            report_data[profile] = stats
            total_posts += stats["total"]
            total_success += stats["success"]
            total_errors += stats["error"]

        profile_sections = ""
        for profile in profiles:
            log_items = ""
            for log in sorted(report_data[profile]["logs"], key=lambda x: x["timestamp"], reverse=True):
                ts = datetime.fromisoformat(log["timestamp"]).strftime("%H:%M:%S")
                msg = f"<br><small>{log['message'][:80]}</small>" if log.get("message") else ""
                log_items += f"""
            <div class="log-item {log.get('status')}">
                <span class="log-time">{ts}</span>
                <strong>{log['action']}</strong> - {log['status']}{msg}
            </div>"""

            profile_sections += f"""
        <div class="profile-section">
            <h2>Profile: {profile}</h2>
            <div class="profile-stats">
                <div class="mini-stat"><div class="number">{report_data[profile]['total']}</div><div class="label">Tong</div></div>
                <div class="mini-stat"><div class="number">{report_data[profile]['success']}</div><div class="label">Thanh cong</div></div>
                <div class="mini-stat"><div class="number">{report_data[profile]['error']}</div><div class="label">Loi</div></div>
            </div>
            <h3 style="margin-top:15px;margin-bottom:10px;color:#555;font-size:1em;">Chi tiet:</h3>
            {log_items}
        </div>"""

        html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f5f5; padding: 20px; color: #333; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px; }}
        .header {{ text-align: center; border-bottom: 3px solid #667eea; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ color: #667eea; margin: 0 0 5px 0; }}
        .header p {{ color: #666; margin: 0; }}
        .summary {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 30px; }}
        .stat-box {{ background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; border-radius: 5px; text-align: center; }}
        .stat-box.success {{ border-left-color: #28a745; }}
        .stat-box.error {{ border-left-color: #dc3545; }}
        .stat-box .number {{ font-size: 2.5em; font-weight: bold; color: #333; }}
        .stat-box .label {{ color: #666; font-size: 0.9em; margin-top: 5px; }}
        .profile-section {{ margin-bottom: 30px; border: 1px solid #ddd; border-radius: 8px; padding: 20px; }}
        .profile-section h2 {{ color: #333; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid #eee; }}
        .profile-stats {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 15px; }}
        .mini-stat {{ background: #f8f9fa; padding: 10px; border-radius: 5px; text-align: center; font-size: 0.9em; }}
        .mini-stat .number {{ font-size: 1.8em; font-weight: bold; color: #333; }}
        .mini-stat .label {{ color: #666; font-size: 0.85em; }}
        .log-item {{ background: #f8f9fa; padding: 12px; margin-bottom: 8px; border-left: 3px solid #ddd; border-radius: 3px; font-size: 0.9em; }}
        .log-item.success {{ border-left-color: #28a745; background: #f0fff4; }}
        .log-item.error {{ border-left-color: #dc3545; background: #fff5f7; }}
        .log-time {{ color: #999; font-size: 0.85em; }}
        .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #999; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>BAO CAO HOAT DONG HANG NGAY</h1>
            <p>{self.today.strftime("%d/%m/%Y - %A")}</p>
        </div>
        <div class="summary">
            <div class="stat-box"><div class="number">{total_posts}</div><div class="label">Tong hoat dong</div></div>
            <div class="stat-box success"><div class="number">{total_success}</div><div class="label">Thanh cong</div></div>
            <div class="stat-box error"><div class="number">{total_errors}</div><div class="label">Loi</div></div>
        </div>
        {profile_sections}
        <div class="footer"><p>TY Automation - Bao cao tu dong</p></div>
    </div>
</body>
</html>"""
        return html, report_data

    def save_report(self):
        html, data = self.generate_html_report()
        report_file = os.path.join(REPORTS_DIR, f"report_{self.today.strftime('%Y%m%d')}.html")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"[OK] Report saved: {report_file}")
        return report_file, data

    def get_summary(self):
        profiles = self.get_all_profiles()
        summary = {"date": self.today.isoformat(), "profiles": {}}
        for profile in profiles:
            logs = self.get_todays_logs(profile)
            summary["profiles"][profile] = {
                "total": len(logs),
                "success": len([l for l in logs if l.get('status') == 'success']),
                "error": len([l for l in logs if l.get('status') == 'error'])
            }
        return summary

    def send_email_report(self, email_to, email_from=None, smtp_password=None):
        if not email_from or not smtp_password:
            print("[!] Email config missing. Skipping.")
            return
        try:
            html, data = self.generate_html_report()
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = email_to
            msg['Subject'] = f"TY Automation - Daily Report [{self.today}]"
            msg.attach(MIMEText(html, 'html', 'utf-8'))
            smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp.login(email_from, smtp_password)
            smtp.send_message(msg)
            smtp.quit()
            print(f"[OK] Report sent to {email_to}")
            return True
        except Exception as e:
            print(f"[!] Error sending email: {e}")
            return False


if __name__ == "__main__":
    generator = ReportGenerator()

    if "--send-email" in sys.argv:
        email_to = os.environ.get("REPORT_EMAIL_TO")
        email_from = os.environ.get("REPORT_EMAIL_FROM")
        email_pass = os.environ.get("REPORT_EMAIL_PASSWORD")
        if email_to and email_from and email_pass:
            generator.send_email_report(email_to, email_from, email_pass)
        else:
            print("[!] Missing email config in .env")

    report_file, data = generator.save_report()

    print("\n" + "="*60)
    print("  DAILY SUMMARY")
    print("="*60)
    summary = generator.get_summary()
    print(f"\nDate: {summary['date']}\n")
    total_posts = sum(p['total'] for p in summary['profiles'].values())
    total_success = sum(p['success'] for p in summary['profiles'].values())
    total_error = sum(p['error'] for p in summary['profiles'].values())
    print(f"Total Posts: {total_posts}")
    print(f"Success:     {total_success}")
    print(f"Errors:      {total_error}\n")
    for profile, stats in summary['profiles'].items():
        print(f"{profile:<15} | Total: {stats['total']:2} | Success: {stats['success']:2} | Error: {stats['error']:2}")
    print("\n" + "="*60)
