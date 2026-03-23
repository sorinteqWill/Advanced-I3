import sys
import subprocess

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {'flask': 'flask', 'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
ensure_deps()
# -------------------------------

from flask import Flask, request
import datetime
from termcolor import colored

app = Flask(__name__)

def log_attack(req):
    timestamp = datetime.datetime.utcnow().isoformat()
    # remote_addr captures the raw TCP socket IP
    attacker_ip = req.remote_addr
    user_agent = req.headers.get('User-Agent', 'Unknown')
    # get_data captures raw POST payloads (exploit attempts)
    payload = req.get_data(as_text=True) 
    
    log_entry = f"[{timestamp}] IP: {attacker_ip} | UA: {user_agent} | Payload: {payload}\n"
    
    # Write to secure local log
    with open("attacker_intel.log", "a") as f:
        f.write(log_entry)
        
    print(colored(f"\n[!] TACTICAL ALERT: INTRUSION DETECTED", "red", attrs=["bold", "blink"]))
    print(colored(f" [+] Origin IP: {attacker_ip}", "yellow"))
    print(f" [+] Target Path: {req.path}")
    print(f" [+] Payload Logged. Awaiting further adversary action...")

# The Catch-All Route: Intercepts EVERYTHING
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    log_attack(request)
    # Return a fake error to keep the attacker interested and engaged
    return '{"error": "Database connection timeout. SQL driver failure. Please try again."}', 500

if __name__ == '__main__':
    print(colored("--- ACTIVE DEFENSE HONEYPOT ONLINE ---", "blue", attrs=["bold"]))
    print("[*] Listening on all interfaces (Port 80).")
    print("[*] Awaiting adversary engagement...")
    # host='0.0.0.0' exposes it to the public internet
    app.run(host='0.0.0.0', port=80)