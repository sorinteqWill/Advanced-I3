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
import random
from termcolor import colored
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_proxies(filepath="proxies.txt"):
    try:
        with open(filepath, 'r') as f:
            # Expecting format: IP:PORT
            proxies = [line.strip() for line in f.readlines() if line.strip()]
        print(colored(f"[*] Loaded {len(proxies)} proxies into the rotation pool.", "blue"))
        return proxies
    except FileNotFoundError:
        print(colored("[-] proxies.txt not found. Create file with IP:PORT list.", "red"))
        return []

def rotated_request(url, proxy_pool):
    if not proxy_pool:
        return
        
    # Select a random proxy from the pool
    selected_proxy = random.choice(proxy_pool)
    proxies = {
        "http": f"socks5h://{selected_proxy}",
        "https": f"socks5h://{selected_proxy}"
    }
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    print(f"[*] Executing strike via node: {selected_proxy}")
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10, verify=False)
        if response.status_code == 200:
            print(colored(f"[✓] Success! Target responded to {selected_proxy}.", "green"))
            return response.text
        else:
            print(colored(f"[-] WAF Blocked {selected_proxy} (HTTP {response.status_code})", "yellow"))
            # In a live script, we would remove the burned proxy from the pool here
    except Exception as e:
        print(colored(f"[-] Node {selected_proxy} is dead or timed out.", "red"))

if __name__ == "__main__":
    print(colored("--- ADVANCED PROXY ROTATION ENGINE ---", "blue", attrs=["bold"]))
    pool = load_proxies()
    if pool:
        # Example Target
        rotated_request("http://mock-investment-scam.com", pool)