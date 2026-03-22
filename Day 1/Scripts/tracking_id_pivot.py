import sys
import subprocess

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
ensure_deps()
# -------------------------------

import re
from termcolor import colored

def find_tracking_ids(html_file_path):
    print(colored("--- SCANNING FOR TRACKING ID PIVOTS ---", "blue"))
    
    try:
        with open(html_file_path, 'r', encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(colored(f"[-] File not found: {html_file_path}. Run stealth_scraper.py first.", "red"))
        return
        
    patterns = {
        "Universal Analytics": r"UA-\d{4,10}-\d{1,4}",
        "GA4 Measurement ID": r"G-[A-Z0-9]{8,12}",
        "Google Tag Manager": r"GTM-[A-Z0-9]{4,7}"
    }
    
    found_intel = False
    for platform, pattern in patterns.items():
        matches = set(re.findall(pattern, content))
        for match in matches:
            found_intel = True
            print(colored(f"[!] {platform} ID Found: {match}", "red", attrs=["bold"]))
            print(f" [*] Pivot Action: Search '{match}' in HackerTarget or BuiltWith to find linked domains.")
            
    if not found_intel:
        print("[-] No common tracking IDs found in the source code.")

if __name__ == "__main__":
    # Analyzes the file downloaded by Script 04
    find_tracking_ids("target_archive.html")