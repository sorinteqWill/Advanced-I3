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

def reverse_analytics_pivot(tracking_id):
    print(colored(f"--- EXECUTING REVERSE ANALYTICS PIVOT ---", "blue", attrs=["bold"]))
    print(f"[*] Target ID: {tracking_id}")
    print("[*] Querying global intelligence databases...")
    
    # Utilizing HackerTarget's free API for reverse analytics
    api_url = f"https://api.hackertarget.com/analyticslookup/?q={tracking_id}"
    
    try:
        response = requests.get(api_url, timeout=15)
        result = response.text.strip()
        
        if "error" in result.lower() or "no results" in result.lower():
            print(colored("[-] No connected domains found in public indexes.", "yellow"))
        elif "API count exceeded" in result:
            print(colored("[-] Free API rate limit exceeded. Switch proxy IP.", "red"))
        else:
            domains = result.split('\n')
            print(colored(f"\n[!] INTELLIGENCE HIT: Found {len(domains)} connected domains:", "green", attrs=["bold"]))
            
            for domain in domains:
                # Format: domain.com, UA-1234567
                clean_domain = domain.split(',')[0]
                print(f" [+] {clean_domain}")
                
            print(colored("\n[*] Pivot Complete. Add these domains to the targeting matrix.", "blue"))
            
    except Exception as e:
        print(colored(f"[-] API connection failed: {e}", "red"))

if __name__ == "__main__":
    # Example Usage: Input the ID found by Script 06
    reverse_analytics_pivot("UA-12345678-1")