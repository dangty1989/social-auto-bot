"""
TY AUTOMATION - Dashboard Web
Giao dien web cho khach hang dang bai Facebook qua trinh duyet
"""
import os, sys, json, subprocess, threading, tempfile
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_PATH = os.path.join(APP_DIR, "engine.py")

load_dotenv(os.path.join(ROOT_DIR, ".env"))

app = Flask(__name__,
            template_folder=os.path.join(APP_DIR, "templates"),
            static_folder=os.path.join(APP_DIR, "static"))
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

PROFILES_DIR = os.environ.get("FB_PROFILES_DIR", os.path.join(ROOT_DIR, "data", "profiles"))
LOGS_DIR = os.environ.get("LOGS_DIR", os.path.join(ROOT_DIR, "data", "logs"))
TEMP_DIR = os.path.join(ROOT_DIR, "data", "temp")

os.makedirs(PROFILES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)


# ============================================================
# API ROUTES
# ============================================================

@app.route("/")
def index():
    profiles = []
    if os.path.exists(PROFILES_DIR):
        profiles = [d for d in os.listdir(PROFILES_DIR) if os.path.isdir(os.path.join(PROFILES_DIR, d))]
    return render_template("dashboard.html", profiles=profiles or ["profile_1"])

@app.route("/api/profiles", methods=["GET"])
def api_get_profiles():
    profiles = []
    if os.path.exists(PROFILES_DIR):
        profiles = sorted([d for d in os.listdir(PROFILES_DIR) if os.path.isdir(os.path.join(PROFILES_DIR, d))])
    return jsonify({"profiles": profiles if profiles else ["profile_1"]})

@app.route("/api/profiles/add", methods=["POST"])
def api_add_profile():
    data = request.json
    profile_name = data.get("name", "").strip()
    if not profile_name or len(profile_name) < 2:
        return jsonify({"status": "error", "message": "Ten profile khong hop le"}), 400
    profile_path = os.path.join(PROFILES_DIR, profile_name)
    if os.path.exists(profile_path):
        return jsonify({"status": "error", "message": "Profile da ton tai"}), 400
    os.makedirs(profile_path, exist_ok=True)
    return jsonify({"status": "success", "profile": profile_name})

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    profile = data.get("profile", "profile_1").strip()

    def run_login():
        try:
            subprocess.run(
                [sys.executable, ENGINE_PATH, "login", "--profile", profile],
                cwd=ROOT_DIR, check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"[LOGIN ERROR] {e}")

    thread = threading.Thread(target=run_login, daemon=True)
    thread.start()
    return jsonify({"status": "success", "message": "Mo Chrome de dang nhap. Dong trinh duyet khi xong."})

@app.route("/api/post/feed", methods=["POST"])
def api_post_feed():
    profile = request.form.get("profile", "profile_1").strip()
    content = request.form.get("content", "").strip()
    private = request.form.get("private", "true").lower() == "true"

    if not content:
        return jsonify({"status": "error", "message": "Noi dung khong duoc trong"}), 400

    media_files = []
    if "media" in request.files:
        files = request.files.getlist("media")
        for file in files:
            if file and file.filename:
                temp_path = os.path.join(TEMP_DIR, file.filename)
                file.save(temp_path)
                media_files.append(temp_path)

    def run_post():
        try:
            cmd = [sys.executable, ENGINE_PATH, "post_feed", "--profile", profile, "--content", content]
            if media_files:
                cmd.extend(["--media", ",".join(media_files)])
            if private:
                cmd.append("--private")
            subprocess.run(cmd, cwd=ROOT_DIR, check=True)
            for f in media_files:
                try:
                    os.remove(f)
                except:
                    pass
        except subprocess.CalledProcessError as e:
            print(f"[POST ERROR] {e}")

    thread = threading.Thread(target=run_post, daemon=True)
    thread.start()
    return jsonify({"status": "success", "message": "Dang thuc hien. Vui long cho..."})

@app.route("/api/post/reel", methods=["POST"])
def api_post_reel():
    profile = request.form.get("profile", "profile_1").strip()
    content = request.form.get("content", "").strip()
    private = request.form.get("private", "true").lower() == "true"

    if "media" not in request.files or not request.files["media"]:
        return jsonify({"status": "error", "message": "Vui long chon video"}), 400
    if not content:
        return jsonify({"status": "error", "message": "Mo ta khong duoc trong"}), 400

    file = request.files["media"]
    temp_path = os.path.join(TEMP_DIR, file.filename)
    file.save(temp_path)

    def run_post_reel():
        try:
            cmd = [sys.executable, ENGINE_PATH, "post_reel", "--profile", profile,
                   "--media", temp_path, "--content", content]
            if private:
                cmd.append("--private")
            subprocess.run(cmd, cwd=ROOT_DIR, check=True)
            try:
                os.remove(temp_path)
            except:
                pass
        except subprocess.CalledProcessError as e:
            print(f"[REEL ERROR] {e}")

    thread = threading.Thread(target=run_post_reel, daemon=True)
    thread.start()
    return jsonify({"status": "success", "message": "Dang thuc hien. Vui long cho..."})

@app.route("/api/logs", methods=["GET"])
def api_get_logs():
    profile = request.args.get("profile", "profile_1")
    log_file = os.path.join(LOGS_DIR, f"{profile}_log.json")
    logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except:
            pass
    return jsonify({"logs": logs[-30:]})


# ============================================================
# TEMPLATE AUTO-CREATE
# ============================================================

def create_templates():
    tpl_dir = os.path.join(APP_DIR, "templates")
    os.makedirs(tpl_dir, exist_ok=True)

    dashboard_html = r"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TY Automation - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: white;
            border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); padding: 30px;
        }
        .header { text-align: center; margin-bottom: 40px; border-bottom: 3px solid #667eea; padding-bottom: 20px; }
        .header h1 { color: #333; font-size: 2.5em; margin-bottom: 5px; }
        .header p { color: #666; font-size: 1.1em; }
        .card {
            background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 8px;
            padding: 25px; transition: all 0.3s ease;
        }
        .card:hover { border-color: #667eea; box-shadow: 0 5px 20px rgba(102,126,234,0.1); }
        .card h2 { color: #333; margin-bottom: 20px; font-size: 1.5em; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 8px; color: #555; font-weight: 500; }
        input[type="text"], input[type="file"], textarea, select {
            width: 100%; padding: 12px; border: 1px solid #ddd;
            border-radius: 6px; font-size: 1em; font-family: inherit;
        }
        textarea { min-height: 120px; resize: vertical; }
        input[type="text"]:focus, textarea:focus, select:focus {
            outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        .checkbox-group { display: flex; align-items: center; gap: 10px; }
        .checkbox-group input[type="checkbox"] { width: auto; cursor: pointer; }
        .checkbox-group label { margin: 0; cursor: pointer; }
        .btn {
            background: #667eea; color: white; padding: 12px 30px; border: none;
            border-radius: 6px; font-size: 1em; font-weight: 600; cursor: pointer;
            transition: all 0.3s ease; width: 100%;
        }
        .btn:hover { background: #764ba2; transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102,126,234,0.3); }
        .btn:disabled { background: #ccc; cursor: not-allowed; transform: none; }
        .btn-secondary { background: #6c757d; margin-top: 10px; }
        .btn-secondary:hover { background: #5a6268; }
        .alert { padding: 15px; border-radius: 6px; margin-bottom: 15px; display: none; }
        .alert.show { display: block; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .alert-info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .logs {
            background: #f8f9fa; border: 1px solid #ddd; border-radius: 6px; padding: 20px;
            max-height: 400px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 0.9em;
        }
        .log-item { padding: 10px; margin-bottom: 8px; border-left: 3px solid #667eea; background: white; border-radius: 3px; }
        .log-item.success { border-left-color: #28a745; }
        .log-item.error { border-left-color: #dc3545; }
        .log-time { color: #999; font-size: 0.85em; }
        .footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e9ecef; color: #999; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>TY Automation Dashboard</h1>
            <p>Dang bai Facebook tu dong</p>
        </div>

        <div class="alert alert-info" id="infoAlert">Vui long dang nhap Facebook lan dau truoc khi dang bai</div>
        <div class="alert alert-success" id="successAlert"></div>
        <div class="alert alert-error" id="errorAlert"></div>

        <div style="margin-bottom: 30px;">
            <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                <label style="margin: 0;">Profile:</label>
                <select id="profileSelect" style="flex: 1; min-width: 200px;">
                    <option value="profile_1">Profile 1</option>
                </select>
                <input type="text" id="newProfileName" placeholder="Ten profile moi..." style="flex: 1; min-width: 200px;">
                <button class="btn" style="flex: 0 1 auto; width: auto;" onclick="addProfile()">+ Them</button>
                <button class="btn btn-secondary" style="flex: 0 1 auto; width: auto;" onclick="loginFacebook()">Dang nhap</button>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
            <div class="card">
                <h2>Dang Bai Thuong</h2>
                <form id="feedForm" onsubmit="postFeed(event)">
                    <div class="form-group">
                        <label>Noi dung bai viet:</label>
                        <textarea id="feedContent" placeholder="Viet noi dung bai viet..." required></textarea>
                    </div>
                    <div class="form-group">
                        <label>Anh / Video (tuy chon):</label>
                        <input type="file" id="feedMedia" multiple accept="image/*,video/*">
                    </div>
                    <div class="form-group checkbox-group">
                        <input type="checkbox" id="feedPrivate" checked>
                        <label for="feedPrivate">Chi minh toi (rieng tu)</label>
                    </div>
                    <button type="submit" class="btn">Dang Bai</button>
                </form>
            </div>

            <div class="card">
                <h2>Dang Reel</h2>
                <form id="reelForm" onsubmit="postReel(event)">
                    <div class="form-group">
                        <label>Video Reel:</label>
                        <input type="file" id="reelMedia" accept="video/*" required>
                    </div>
                    <div class="form-group">
                        <label>Mo ta:</label>
                        <textarea id="reelContent" placeholder="Mo ta reel..." required></textarea>
                    </div>
                    <div class="form-group checkbox-group">
                        <input type="checkbox" id="reelPrivate" checked>
                        <label for="reelPrivate">Chi minh toi (rieng tu)</label>
                    </div>
                    <button type="submit" class="btn">Dang Reel</button>
                </form>
            </div>
        </div>

        <div class="card" style="margin-top: 30px;">
            <h2>Lich su hoat dong</h2>
            <div class="logs" id="logsContainer">
                <div style="color: #999;">Chua co hoat dong nao...</div>
            </div>
            <button class="btn btn-secondary" onclick="refreshLogs()">Lam moi</button>
        </div>

        <div class="footer">
            <p>TY Automation | Web Dashboard v2.0</p>
        </div>
    </div>

    <script>
        let currentProfile = "profile_1";

        document.addEventListener("DOMContentLoaded", () => {
            loadProfiles();
            refreshLogs();
            setInterval(refreshLogs, 5000);
        });

        async function loadProfiles() {
            try {
                const res = await fetch("/api/profiles");
                const data = await res.json();
                const select = document.getElementById("profileSelect");
                select.innerHTML = '';
                data.profiles.forEach(p => {
                    select.innerHTML += '<option value="' + p + '">' + p + '</option>';
                });
                currentProfile = data.profiles[0];
            } catch(e) { console.error(e); }
        }

        async function addProfile() {
            const name = document.getElementById("newProfileName").value.trim();
            if (!name) return alert("Nhap ten profile");
            try {
                const res = await fetch("/api/profiles/add", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name })
                });
                const data = await res.json();
                if (data.status === "success") {
                    showAlert("Them profile thanh cong", "success");
                    document.getElementById("newProfileName").value = '';
                    loadProfiles();
                } else { showAlert(data.message, "error"); }
            } catch(e) { showAlert("Loi: " + e, "error"); }
        }

        async function loginFacebook() {
            const profile = document.getElementById("profileSelect").value;
            try {
                const res = await fetch("/api/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ profile })
                });
                showAlert("Chrome vua mo. Dang nhap Facebook roi DONG TRINH DUYET de luu phien.", "info");
            } catch(e) { showAlert("Loi: " + e, "error"); }
        }

        async function postFeed(e) {
            e.preventDefault();
            const profile = document.getElementById("profileSelect").value;
            const content = document.getElementById("feedContent").value;
            const media = document.getElementById("feedMedia").files;
            const priv = document.getElementById("feedPrivate").checked;

            const form = new FormData();
            form.append("profile", profile);
            form.append("content", content);
            form.append("private", priv);
            for (let file of media) form.append("media", file);

            try {
                const res = await fetch("/api/post/feed", { method: "POST", body: form });
                const data = await res.json();
                if (data.status === "success") {
                    showAlert("Dang dang bai... Vui long cho", "success");
                    document.getElementById("feedForm").reset();
                    setTimeout(refreshLogs, 3000);
                } else { showAlert(data.message, "error"); }
            } catch(e) { showAlert("Loi: " + e, "error"); }
        }

        async function postReel(e) {
            e.preventDefault();
            const profile = document.getElementById("profileSelect").value;
            const content = document.getElementById("reelContent").value;
            const media = document.getElementById("reelMedia").files[0];
            const priv = document.getElementById("reelPrivate").checked;
            if (!media) return alert("Chon video");

            const form = new FormData();
            form.append("profile", profile);
            form.append("content", content);
            form.append("media", media);
            form.append("private", priv);

            try {
                const res = await fetch("/api/post/reel", { method: "POST", body: form });
                const data = await res.json();
                if (data.status === "success") {
                    showAlert("Dang dang Reel... Vui long cho", "success");
                    document.getElementById("reelForm").reset();
                    setTimeout(refreshLogs, 3000);
                } else { showAlert(data.message, "error"); }
            } catch(e) { showAlert("Loi: " + e, "error"); }
        }

        async function refreshLogs() {
            const profile = document.getElementById("profileSelect").value;
            try {
                const res = await fetch("/api/logs?profile=" + profile);
                const data = await res.json();
                const logsDiv = document.getElementById("logsContainer");
                if (data.logs.length === 0) {
                    logsDiv.innerHTML = '<div style="color: #999;">Chua co hoat dong nao...</div>';
                    return;
                }
                logsDiv.innerHTML = data.logs.map(log =>
                    '<div class="log-item ' + log.status + '">' +
                    '<span class="log-time">' + new Date(log.timestamp).toLocaleString('vi-VN') + '</span> ' +
                    '<strong>' + log.action + '</strong> - ' + log.status +
                    (log.message ? '<br><small>' + log.message + '</small>' : '') +
                    '</div>'
                ).reverse().join('');
            } catch(e) { console.error(e); }
        }

        function showAlert(msg, type) {
            const alerts = {
                success: document.getElementById("successAlert"),
                error: document.getElementById("errorAlert"),
                info: document.getElementById("infoAlert")
            };
            const el = alerts[type];
            if (el) {
                el.textContent = msg;
                el.classList.add("show");
                setTimeout(() => el.classList.remove("show"), 5000);
            }
        }

        document.getElementById("profileSelect").addEventListener("change", (e) => {
            currentProfile = e.target.value;
            refreshLogs();
        });
    </script>
</body>
</html>"""

    tpl_file = os.path.join(tpl_dir, "dashboard.html")
    with open(tpl_file, "w", encoding="utf-8") as f:
        f.write(dashboard_html)
    print("[OK] Templates created")


if __name__ == "__main__":
    create_templates()

    port = int(os.environ.get("FLASK_PORT", 5000))
    host = os.environ.get("FLASK_HOST", "127.0.0.1")

    print("\n" + "="*60)
    print("  TY AUTOMATION - DASHBOARD")
    print("="*60)
    print(f"\n[*] Dang chay tren: http://{host}:{port}")
    print("[!] Ctrl+C de dung server\n")

    app.run(host=host, port=port, debug=False)
