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
import time
import random
from termcolor import colored
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fuzz_api_endpoints(base_url):
    print(colored(f"--- INITIATING TACTICAL API FUZZER: {base_url} ---", "blue", attrs=["bold"]))
    
    # Ensure URL formatting
    if not base_url.endswith('/'):
        base_url += '/'
        
    # Curated High-Value Target Dictionary
    endpoints = [
        ".env", "admin/", "administrator/", "api/v1/users", "api/v2/users",
        "debug/", "phpinfo.php", "backup.zip", "db.sql", "config.bak",
        ".git/config", "server-status", "api/swagger.json", "logs/"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    hits_found = 0
    
    for path in endpoints:
        target_url = f"{base_url}{path}"
        try:
            response = requests.get(target_url, headers=headers, timeout=10, verify=False)
            
            # 200 OK means the file exists and is accessible
            if response.status_code == 200:
                # Basic false-positive check (Is it just returning the HTML homepage?)
                if "html" not in response.headers.get("Content-Type", "").lower() or path.endswith("/"):
                    print(colored(f"\n[!] CRITICAL EXPOSURE FOUND: {target_url}", "green", attrs=["bold"]))
                    print(f" [+] HTTP 200 OK. Snippet: {response.text[:100].strip()}...")
                    hits_found += 1
                else:
                    # It returned 200, but it's just an HTML page (likely a custom 404)
                    print(colored(f" [-] False Positive 200 OK at {path}", "yellow"))
                    
            # 403 means it exists, but we are blocked. Still good intelligence.
            elif response.status_code == 403:
                print(colored(f" [!] Access Forbidden (403), but directory exists: {target_url}", "yellow"))
                
            time.sleep(random.uniform(0.5, 1.5)) # Anti-WAF delay
            
        except requests.exceptions.RequestException as e:
            print(colored(f" [-] Connection failed on {path}", "red"))
            
    if hits_found == 0:
        print(colored("\n[-] Fuzzing complete. No critical unauthenticated endpoints exposed.", "yellow"))
    else:
        print(colored(f"\n[✓] Fuzzing complete. {hits_found} exposed assets confirmed.", "blue", attrs=["bold"]))

if __name__ == "__main__":
    # Example usage: Insert the true Origin IP found by the CT Searcher
    fuzz_api_endpoints("http://192.168.1.100")