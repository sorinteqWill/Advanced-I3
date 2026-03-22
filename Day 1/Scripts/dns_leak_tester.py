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

def check_dns_leaks():
    print(colored("--- EXECUTING KERNEL DNS LEAK TEST ---", "blue", attrs=["bold"]))
    try:
        response = requests.get("https://bash.ws/dnsleak/test/myip", timeout=15)
        dns_data = response.json()
        
        print(f"[*] Broadcasted IP: {dns_data.get('ip')}")
        print(colored("[*] Resolving DNS Servers Intercepted:", "yellow"))
        
        leak_detected = False
        for dns in dns_data.get('dns', []):
            country = dns.get('country', 'Unknown')
            asn = dns.get('asn', 'Unknown')
            print(f" [+] DNS Node: {dns.get('ip')} ({country} | {asn})")
            
            if "United Kingdom" in country or "UK" in country:
                leak_detected = True
                
        if leak_detected:
            print(colored("\n[!] CRITICAL OPSEC FAILURE: Local ISP DNS Leak Detected!", "red", attrs=["bold"]))
            print("[-] Abort operation. Check /etc/proxychains4.conf 'proxy_dns' setting.")
        else:
            print(colored("\n[✓] DNS Routing Sealed. No local leaks detected.", "green"))
            
    except Exception as e:
        print(colored(f"[-] Network Error or Proxy Block: {e}", "red"))

if __name__ == "__main__":
    check_dns_leaks()