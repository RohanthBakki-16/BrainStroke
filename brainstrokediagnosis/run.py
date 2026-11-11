#!/usr/bin/env python
"""
NeuroScan AI - Brain Stroke Detection System
Runner Script: Launches the Django development server and automatically opens
the web application in a new browser tab.
"""

import os
import sys
import time
import socket
import threading
import webbrowser
import subprocess
from pathlib import Path

# Paths determination
BASE_DIR = Path(__file__).resolve().parent

# Check if manage.py is in current folder or in brainstrokediagnosis subfolder
if (BASE_DIR / "brainstrokediagnosis" / "manage.py").exists():
    PROJECT_DIR = BASE_DIR / "brainstrokediagnosis"
    VENV_DIR = BASE_DIR / "venv"
elif (BASE_DIR / "manage.py").exists():
    PROJECT_DIR = BASE_DIR
    VENV_DIR = BASE_DIR.parent / "venv"
else:
    PROJECT_DIR = BASE_DIR
    VENV_DIR = BASE_DIR / "venv"

# Determine python executable (prefer project virtualenv if exists)
if sys.platform == "win32":
    venv_python = VENV_DIR / "Scripts" / "python.exe"
else:
    venv_python = VENV_DIR / "bin" / "python"

# If we are not currently running under the virtualenv python and it exists, re-launch with it
if venv_python.exists() and Path(sys.executable).resolve() != venv_python.resolve():
    print(f"[*] Activating virtual environment: {venv_python}")
    try:
        result = subprocess.run([str(venv_python), __file__] + sys.argv[1:])
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(0)

# Server configuration
HOST = "127.0.0.1"
PORT = 8000
SERVER_URL = f"http://{HOST}:{PORT}/"
MANAGE_PY = PROJECT_DIR / "manage.py"


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def auto_open_browser():
    """Waits for the server to become responsive, then opens the browser."""
    print(f"[*] Waiting for server to initialize at {SERVER_URL}...")
    start_time = time.time()
    opened = False

    while time.time() - start_time < 30:
        if is_port_in_use(PORT, HOST):
            time.sleep(0.8)  # Short breather for Django to finish route loading
            print(f"[*] Server is live! Opening {SERVER_URL} in your default browser...")
            webbrowser.open_new_tab(SERVER_URL)
            opened = True
            break
        time.sleep(0.4)

    if not opened:
        print(f"[!] Server took too long to start. You can open manually at: {SERVER_URL}")


def main():
    print("=" * 68)
    print("      NEUROSCAN AI - BRAIN STROKE DETECTION & DIAGNOSTIC SYSTEM      ")
    print("=" * 68)
    print(f" [*] Project Directory: {PROJECT_DIR}")
    print(f" [*] Local Server URL:  {SERVER_URL}")
    print(" [*] Auto Browser:     Enabled (opens in new tab)")
    print(" [*] Stop Server:       Press Ctrl+C anytime")
    print("=" * 68)

    # Launch browser opener in background thread
    opener_thread = threading.Thread(target=auto_open_browser, daemon=True)
    opener_thread.start()

    # Run Django development server
    try:
        subprocess.run(
            [sys.executable, str(MANAGE_PY), "runserver", f"{HOST}:{PORT}"],
            cwd=str(PROJECT_DIR)
        )
    except KeyboardInterrupt:
        print("\n[*] Server stopped gracefully. Goodbye!")
    except Exception as e:
        print(f"\n[!] Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
