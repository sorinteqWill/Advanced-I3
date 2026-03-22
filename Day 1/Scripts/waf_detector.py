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

def detect_waf(url):
    print(colored(f"--- WAF RECONNAISSANCE: {url} ---", "blue", attrs=["bold"]))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        server_header = response.headers.get('Server', '').lower()
        cookies = response.cookies.get_dict()
        
        waf_found = False
        
        if 'cloudflare' in server_header:
            print(colored("[!] TARGET SHIELDED BY CLOUDFLARE", "red"))
            waf_found = True
        elif 'imperva' in server_header or 'incapsula' in server_header:
            print(colored("[!] TARGET SHIELDED BY IMPERVA", "red"))
            waf_found = True
            
        if 'cf_clearance' in cookies or '__cfduid' in cookies:
            print(colored("[!] CLOUDFLARE BOT-MANAGEMENT COOKIES DETECTED", "red"))
            waf_found = True
            
        if not waf_found:
            print(colored("[✓] No standard WAF signatures detected in headers.", "green"))
            print("[*] Target is cleared for stealth_scraper.py execution.")
        else:
            print("[*] Tactical Advice: Adjust stealth_scraper.py sleep timers to avoid rate-limiting bans.")
            
    except Exception as e:
        print(colored(f"[-] Request failed. Target is dropping automated pings: {e}", "red"))

if __name__ == "__main__":
    # Example usage: Change URL to target
    detect_waf("http://mock-investment-scam.com")