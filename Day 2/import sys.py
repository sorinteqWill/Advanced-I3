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
import socket
from termcolor import colored

def query_ct_logs(target_domain):
    print(colored(f"--- INITIATING CERTIFICATE TRANSPARENCY SEARCH: {target_domain} ---", "blue", attrs=["bold"]))
    
    # Query crt.sh for JSON output
    url = f"https://crt.sh/?q={target_domain}&output=json"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            print(colored(f"[-] API Error: crt.sh returned HTTP {response.status_code}", "red"))
            return
            
        data = response.json()
        unique_subdomains = set()
        
        # Parse all issued certificates
        for entry in data:
            name_value = entry.get('name_value', '')
            # Handle multi-domain certificates separated by newlines
            domains = name_value.split('\n')
            for d in domains:
                clean_domain = d.strip()
                # Ignore wildcards as they cannot be resolved directly
                if clean_domain and not clean_domain.startswith('*'):
                    unique_subdomains.add(clean_domain)
                    
        print(f"[*] Discovered {len(unique_subdomains)} historical subdomains.")
        print(colored("[*] Initiating live DNS resolution to identify Origin IP leaks...", "yellow"))
        
        # Cloudflare common IP prefixes (Simplified for lab environment)
        cf_prefixes = ('104.', '172.', '188.', '162.', '198.41')
        
        for sub in unique_subdomains:
            try:
                ip_addr = socket.gethostbyname(sub)
                
                if str(ip_addr).startswith(cf_prefixes):
                    print(f" [+] {sub} -> {ip_addr} (Proxied/Shielded)")
                else:
                    # If it's not a known CF prefix, it might be the true Origin
                    print(colored(f" [!] EXPOSED ORIGIN: {sub} -> {ip_addr}", "red", attrs=["bold"]))
            except socket.gaierror:
                # Subdomain exists in logs, but is no longer actively resolving
                pass
                
        print(colored("\n[✓] Certificate Transparency Search Complete.", "green"))

    except Exception as e:
        print(colored(f"[-] Fatal error querying CT logs: {e}", "red"))

if __name__ == "__main__":
    # Example usage: Target domain
    query_ct_logs("target-scam-domain.com")