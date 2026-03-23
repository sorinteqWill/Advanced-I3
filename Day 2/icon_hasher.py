import sys
import subprocess

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {'requests': 'requests', 'mmh3': 'mmh3', 'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
ensure_deps()
# -------------------------------

import requests
import mmh3
import codecs
from termcolor import colored
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def calculate_favicon_hash(url):
    print(colored("--- VISUAL INFRASTRUCTURE HASHER ---", "blue", attrs=["bold"]))
    
    # Ensure URL targets the standard favicon path
    if not url.endswith('/'):
        url += '/'
    icon_url = f"{url}favicon.ico"
    
    print(f"[*] Targeting visual asset: {icon_url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(icon_url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            print(colored("[*] Asset acquired. Generating MurmurHash3 signature...", "yellow"))
            
            # Shodan specific hash calculation:
            # 1. Base64 encode the raw binary image content
            favicon_b64 = codecs.encode(response.content, 'base64')
            
            # 2. Hash the Base64 string using mmh3
            hash_value = mmh3.hash(favicon_b64)
            
            print(colored(f"\n[!] HIGH-VALUE INTELLIGENCE GENERATED:", "green", attrs=["bold"]))
            print(f" [+] Mathematical Signature: {hash_value}")
            print(colored(f" [+] Shodan Dork: http.favicon.hash:{hash_value}", "cyan", attrs=["bold"]))
            print("\n[*] Pivot Action: Enter the Dork into Shodan.io to locate linked servers.")
            
        else:
            print(colored(f"[-] Asset not found at default path (HTTP {response.status_code})", "red"))
            print("[*] Tactical Advice: Parse the site's HTML <link rel='icon'> tag for custom paths.")
            
    except Exception as e:
        print(colored(f"[-] Network connection failed: {e}", "red"))

if __name__ == "__main__":
    # Example usage: Target the main domain, script will append favicon.ico
    calculate_favicon_hash("http://mock-investment-scam.com")