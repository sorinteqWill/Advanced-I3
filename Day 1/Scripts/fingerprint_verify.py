import requests
import json
from termcolor import colored

def check_leaks():
    # Targets that report back what your browser/script is 'bleeding'
    endpoints = {
        "IP/ISP": "https://ipapi.co/json/",
        "User-Agent": "https://httpbin.org/user-agent",
        "Headers": "https://httpbin.org/get"
    }
    
    print(colored("--- OSINT VM PRE-FLIGHT LEAK CHECK ---", "blue", attrs=["bold"]))
    
    try:
        # Check IP and ISP reputation
        ip_data = requests.get(endpoints["IP/ISP"]).json()
        print(f"[+] Reported IP: {ip_data.get('ip')}")
        print(f"[+] Reported ISP: {ip_data.get('org')}")
        
        # LOGIC: Flag if the ISP matches a known UK Law Enforcement or Residential block
        if "Metropolitan" in ip_data.get('org') or "Home Office" in ip_data.get('org'):
            print(colored("[!] CRITICAL LEAK: Real Department ISP Detected!", "red", attrs=["blink"]))
        else:
            print(colored("[✓] Network Masking: Active", "green"))

        # Check User-Agent consistency
        ua = requests.get(endpoints["User-Agent"]).json()
        print(f"[+] Outgoing User-Agent: {ua.get('user-agent')}")
        
    except Exception as e:
        print(colored(f"[-] Connection Error: {e}", "red"))

if __name__ == "__main__":
    check_leaks()