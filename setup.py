#!/usr/bin/env python3
import os
import subprocess
import sys

PROJECT_NAME = "REDSHELL"
DEVELOPER = "Leptip 💻"
OUTPUT_DIR = "output"

def check_install_package(package):
    try:
        __import__(package)
        print(f"[✓] Python package '{package}' is already installed.")
    except ImportError:
        print(f"[i] Installing Python package '{package}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_mcs():
    try:
        subprocess.run(["mcs", "-help"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("[✓] 'mcs' (Mono C# Compiler) is available.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[!] 'mcs' not found. Please install mono-complete:")
        print("    sudo apt update && sudo apt install mono-complete")
        sys.exit(1)

def main():
    print(f"\n=== Installing {PROJECT_NAME} ===")
    print(f"Developer: {DEVELOPER}\n")

    # 1️⃣ Install Python dependencies
    check_install_package("colorama")

    # 2️⃣ Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"[✓] Output directory '{OUTPUT_DIR}' is ready.\n")

    # 3️⃣ Check Mono C# compiler
    check_mcs()

    print(f"\n[✓] {PROJECT_NAME} setup completed successfully!")
    print(f"[i] You can now run main.py to generate PowerShell/EXE payloads.\n")

if __name__ == "__main__":
    main()
