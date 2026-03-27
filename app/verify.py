"""
TY AUTOMATION - System Verification
Kiem tra he thong truoc khi su dung
"""
import os, sys, json, subprocess
from pathlib import Path
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SystemVerifier:
    def __init__(self):
        self.checks = []
        self.root_dir = Path(ROOT_DIR)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def check(self, name, condition, error_msg=""):
        status = "OK" if condition else "FAIL"
        self.checks.append({"name": name, "passed": condition, "error": error_msg if not condition else ""})
        if condition:
            print(f"  [OK]   {name}")
        else:
            print(f"  [FAIL] {name}")
            if error_msg:
                print(f"         -> {error_msg}")

    def verify_python(self):
        print("\n[1] PYTHON")
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            version = result.stdout.strip() or result.stderr.strip()
            self.check("Python installed", True)
            print(f"         {version}")
        except Exception as e:
            self.check("Python installed", False, str(e))

    def verify_packages(self):
        print("\n[2] PYTHON PACKAGES")
        packages = [
            ("playwright", "playwright"),
            ("playwright_stealth", "playwright-stealth"),
            ("dotenv", "python-dotenv"),
            ("requests", "requests"),
            ("flask", "flask"),
            ("schedule", "schedule"),
        ]
        for module, pip_name in packages:
            try:
                __import__(module)
                self.check(f"Package: {pip_name}", True)
            except ImportError:
                self.check(f"Package: {pip_name}", False, f"pip install {pip_name}")

    def verify_files(self):
        print("\n[3] FILES")
        essential = {
            "app/engine.py": self.root_dir / "app" / "engine.py",
            "app/dashboard.py": self.root_dir / "app" / "dashboard.py",
            "app/scheduler.py": self.root_dir / "app" / "scheduler.py",
            "app/report.py": self.root_dir / "app" / "report.py",
            "requirements.txt": self.root_dir / "requirements.txt",
            ".env.example": self.root_dir / ".env.example",
        }
        for name, path in essential.items():
            self.check(f"File: {name}", path.exists(), "Missing!")

    def verify_directories(self):
        print("\n[4] DIRECTORIES")
        dirs = {
            "data/profiles": self.root_dir / "data" / "profiles",
            "data/logs": self.root_dir / "data" / "logs",
            "data/reports": self.root_dir / "data" / "reports",
            "data/schedules": self.root_dir / "data" / "schedules",
        }
        for name, path in dirs.items():
            try:
                path.mkdir(parents=True, exist_ok=True)
                self.check(f"Dir: {name}", path.exists())
            except Exception as e:
                self.check(f"Dir: {name}", False, str(e))

    def verify_env(self):
        print("\n[5] ENV CONFIG")
        env_path = self.root_dir / ".env"
        if env_path.exists():
            self.check(".env exists", True)
            try:
                with open(env_path, 'r') as f:
                    content = f.read()
                self.check(".env has FB_PROFILES_DIR", "FB_PROFILES_DIR" in content)
                self.check(".env has FLASK_PORT", "FLASK_PORT" in content)
            except Exception as e:
                self.check(".env readable", False, str(e))
        else:
            self.check(".env exists", False, "Run SETUP.bat first")

    def verify_permissions(self):
        print("\n[6] PERMISSIONS")
        test_file = self.root_dir / "data" / "test_write.tmp"
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            test_file.unlink()
            self.check("Write permission", True)
        except Exception as e:
            self.check("Write permission", False, str(e))

    def run(self):
        print("\n" + "="*60)
        print("  TY AUTOMATION - SYSTEM CHECK")
        print("="*60)

        self.verify_python()
        self.verify_packages()
        self.verify_files()
        self.verify_directories()
        self.verify_env()
        self.verify_permissions()

        total = len(self.checks)
        passed = sum(1 for c in self.checks if c["passed"])
        failed = total - passed

        print("\n" + "="*60)
        print(f"  RESULT: {passed}/{total} passed")
        print("="*60)

        if failed > 0:
            print("\n  FAILURES:")
            for c in self.checks:
                if not c["passed"]:
                    print(f"  - {c['name']}: {c['error']}")
            print("\n  FIX: Run SETUP.bat first")

        if failed == 0:
            print("\n  SYSTEM STATUS: ALL OK")
        else:
            print(f"\n  SYSTEM STATUS: {failed} ISSUES")

        print("="*60 + "\n")
        return 0 if failed == 0 else 1


if __name__ == "__main__":
    verifier = SystemVerifier()
    sys.exit(verifier.run())
