import sys
import subprocess
import shutil

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

import json
from termcolor import colored

def harvest_metadata(file_path):
    print(colored(f"--- HARVESTING METADATA FROM: {file_path} ---", "blue"))
    
    # Check for system-level dependency
    if not shutil.which("exiftool"):
        print(colored("[-] CRITICAL: 'exiftool' is not installed on this Linux system.", "red"))
        print("[*] Run the following command in your terminal first:")
        print("    sudo apt-get install libimage-exiftool-perl")
        return

    try:
        result = subprocess.run(['exiftool', '-j', file_path], capture_output=True, text=True)
        metadata = json.loads(result.stdout)[0]
        
        author = metadata.get("Author", "N/A")
        creator_tool = metadata.get("CreatorTool", "N/A")
        create_date = metadata.get("CreateDate", "N/A")
        
        print(colored("[!] HIGH-VALUE INTEL FOUND:", "green", attrs=["bold"]))
        print(f" [+] Author/Username: {author}")
        print(f" [+] Software Used: {creator_tool}")
        print(f" [+] Creation Date: {create_date}")
        
    except Exception as e:
        print(f"[-] Error parsing metadata. Is the file path correct? ({e})")

if __name__ == "__main__":
    # Example usage: Update with the actual path to your downloaded document
    harvest_metadata("scam_whitepaper.pdf")