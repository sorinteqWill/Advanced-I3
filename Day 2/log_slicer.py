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

import mmap
import os
from termcolor import colored

def execute_log_slice(file_path, search_string, max_hits=50):
    print(colored(f"--- INITIATING INDUSTRIAL LOG SLICER ---", "blue", attrs=["bold"]))
    print(f"[*] Target File: {file_path}")
    print(f"[*] Artifact Signature: '{search_string}'")
    
    if not os.path.exists(file_path):
        print(colored("[-] Critical Error: Log file not found.", "red"))
        return
        
    target_bytes = search_string.encode('utf-8')
    hit_count = 0
    
    print(colored("[*] Memory mapping file to kernel... initiating high-speed sweep.", "yellow"))
    
    try:
        # Open in binary read mode
        with open(file_path, "rb") as f:
            # Create the memory map
            with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
                
                # Start searching from the beginning (index 0)
                current_pos = 0
                
                with open("sliced_intel.log", "w") as out_log:
                    while hit_count < max_hits:
                        # Find the byte index of the target
                        hit_index = mm.find(target_bytes, current_pos)
                        
                        if hit_index == -1:
                            break # No more instances found
                            
                        # Locate the start of the line (previous newline character)
                        line_start = mm.rfind(b'\n', 0, hit_index)
                        if line_start == -1:
                            line_start = 0 # It's the very first line
                        else:
                            line_start += 1 # Move past the newline char
                            
                        # Locate the end of the line (next newline character)
                        line_end = mm.find(b'\n', hit_index)
                        if line_end == -1:
                            line_end = len(mm) # It's the very last line
                            
                        # Slice the raw bytes and decode to text
                        raw_line = mm[line_start:line_end]
                        decoded_line = raw_line.decode('utf-8', errors='ignore').strip()
                        
                        print(colored(f"[!] ARTIFACT EXTRACTED:", "green"))
                        print(f"    {decoded_line}")
                        
                        out_log.write(f"{decoded_line}\n")
                        
                        hit_count += 1
                        current_pos = line_end # Move pointer to continue searching
                        
        if hit_count == 0:
            print(colored("\n[-] Sweep complete. Target artifact not present in logs.", "yellow"))
        elif hit_count >= max_hits:
            print(colored(f"\n[!] Maximum safe display cap reached ({max_hits} hits).", "yellow"))
            print("[*] Further hits were suppressed. Review sliced_intel.log for details.")
        else:
            print(colored(f"\n[✓] Sweep complete. Total hits extracted: {hit_count}", "blue", attrs=["bold"]))

    except Exception as e:
        print(colored(f"[-] Fatal Slicing Error: {e}", "red"))

if __name__ == "__main__":
    # Example usage: Searching a hypothetical seized Apache log for a specific username
    # Create a dummy text file named 'seized_server.log' to test locally.
    execute_log_slice("seized_server.log", "admin_login_attempt")