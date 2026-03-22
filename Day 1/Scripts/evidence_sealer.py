import sys
import subprocess

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
ensure_deps()
# -------------------------------

import os
import hashlib
from datetime import datetime
from termcolor import colored

def hash_file(filepath):
    """Generates a SHA-256 hash for a given file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

def seal_evidence():
    print(colored("--- EXECUTING CRYPTOGRAPHIC EVIDENCE SEAL ---", "blue", attrs=["bold"]))
    
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    manifest_name = f"Evidence_Manifest_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    
    targets = ["target_archive.html"]
    vault_dir = "forensic_vault"
    
    if os.path.exists(vault_dir):
        for root, dirs, files in os.walk(vault_dir):
            for file in files:
                targets.append(os.path.join(root, file))
                
    if not targets or (len(targets) == 1 and not os.path.exists(targets[0])):
        print(colored("[-] No evidence found in the current directory to seal.", "red"))
        return

    print(f"[*] Hashing {len(targets)} forensic assets...")
    
    with open(manifest_name, "w") as manifest:
        manifest.write(f"==================================================\n")
        manifest.write(f" LAW ENFORCEMENT DIGITAL EVIDENCE MANIFEST\n")
        manifest.write(f"==================================================\n")
        manifest.write(f"Sealed On: {timestamp}\n")
        manifest.write(f"Algorithm: SHA-256\n")
        manifest.write(f"==================================================\n\n")
        
        for target in targets:
            if os.path.exists(target):
                file_hash = hash_file(target)
                log_entry = f"FILE: {target}\nHASH: {file_hash}\n\n"
                manifest.write(log_entry)
                print(colored(f" [+] {target} -> {file_hash[:16]}...", "green"))
            else:
                print(colored(f" [-] {target} not found. Skipping.", "yellow"))
                
    print(colored(f"\n[✓] Chain of custody established. Manifest saved as: {manifest_name}", "blue", attrs=["bold"]))

if __name__ == "__main__":
    seal_evidence()