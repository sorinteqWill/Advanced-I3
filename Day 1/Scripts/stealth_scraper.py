import sys
import subprocess

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {'requests': 'requests', 'beautifulsoup4': 'bs4', 'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
ensure_deps()
# -------------------------------

import requests
from bs4 import BeautifulSoup
from termcolor import colored
import urllib3

# Suppress insecure request warnings for offline scraping of bad certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def stealth_scrape(url):
    print(colored(f"--- EXECUTING STEALTH SCRAPE ON {url} ---", "blue"))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = soup.find_all('a', href=True)
        print(colored(f"[✓] Extracted {len(links)} internal/external links.", "green"))
        
        with open("target_archive.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
            
        print("[*] Raw HTML saved to target_archive.html for offline analysis.")
        
    except Exception as e:
        print(colored(f"[-] Scrape failed: {e}", "red"))

if __name__ == "__main__":
    # Example usage: Change URL to target
    stealth_scrape("http://mock-investment-scam.com")