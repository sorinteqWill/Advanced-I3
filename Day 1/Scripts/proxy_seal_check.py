import sys
import subprocess

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {'requests': 'requests', 'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
ensure_deps()
# -------------------------------

import requests
from termcolor import colored

def verify_opsec_seal():
    print(colored("--- VERIFYING TERMINAL OPSEC SEAL ---", "blue", attrs=["bold"]))
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=10)
        ip_data = response.json()
        current_ip = ip_data.get('ip')
        
        print(f"[*] Python is broadcasting IP: {current_ip}")
        print(colored("[!] WARNING: If this is your real IP or Department IP, ABORT IMMEDIATELY.", "yellow"))
        print("[*] Ensure you are running this script via 'proxychains python3 script.py'")
        
    except Exception as e:
        print(colored(f"[-] Network Error: {e}. Proxy may be blocking the connection.", "red"))

if __name__ == "__main__":
    verify_opsec_seal()