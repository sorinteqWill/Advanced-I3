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

from termcolor import colored

def find_mutuals(file1, file2):
    print(colored(f"--- SOCIAL NETWORK LINK ANALYSIS ---", "blue", attrs=["bold"]))
    
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            set1 = set(line.strip().lower() for line in f1 if line.strip())
            set2 = set(line.strip().lower() for line in f2 if line.strip())
            
        mutuals = set1.intersection(set2)
        
        print(f"[*] Suspect A Associates: {len(set1)}")
        print(f"[*] Suspect B Associates: {len(set2)}")
        
        print(colored(f"\n[!] MUTUAL ASSOCIATES IDENTIFIED: {len(mutuals)}", "green", attrs=["bold"]))
        for person in mutuals:
            print(f" [+] {person}")
            
    except Exception as e:
        print(colored(f"[-] Error: {e}", "red"))

if __name__ == "__main__":
    # Create dummy files for demonstration
    with open("a.txt", "w") as f: f.write("admin_v\nscam_king\njohn_doe\nmule_1")
    with open("b.txt", "w") as f: f.write("mule_1\nadmin_v\nrandom_user\nshady_dealer")
    
    find_mutuals("a.txt", "b.txt")