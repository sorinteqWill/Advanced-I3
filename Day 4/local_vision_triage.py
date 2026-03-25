import sys
import subprocess
import os

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    # easyocr heavily relies on torch and opencv-python-headless
    deps = {'easyocr': 'easyocr', 'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
ensure_deps()
# -------------------------------

import easyocr
from termcolor import colored

def execute_vision_triage(directory_path):
    print(colored(f"--- INITIATING LOCAL AI VISION TRIAGE ---", "blue", attrs=["bold"]))
    print(f"[*] Target Vault: {directory_path}")
    
    if not os.path.exists(directory_path):
        print(colored("[-] Critical Error: Vault directory not found.", "red"))
        return

    print(colored("[*] Loading PyTorch Deep Learning Model into RAM...", "yellow"))
    print("[*] (Note: GPU acceleration is disabled for maximum hardware compatibility)")
    
    # Initialize the OCR reader for English. Downloads model on first run only.
    try:
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    except Exception as e:
        print(colored(f"[-] AI Model Initialization Failed: {e}", "red"))
        return
        
    supported_formats = ('.png', '.jpg', '.jpeg')
    images_processed = 0
    text_blocks_found = 0
    
    output_log = "Vision_Triage_Log.txt"
    
    with open(output_log, "w", encoding="utf-8") as out:
        out.write("=========================================\n")
        out.write(" LOCAL AI VISION TRIAGE EXTRACTION LOG\n")
        out.write("=========================================\n\n")
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith(supported_formats):
                    img_path = os.path.join(root, file)
                    print(f" [*] Scanning -> {file}...")
                    
                    try:
                        # Perform the inference
                        results = reader.readtext(img_path)
                        
                        if results:
                            out.write(f"--- SOURCE FILE: {file} ---\n")
                            
                            for (bbox, text, confidence) in results:
                                # Only log high-confidence extractions to avoid AI noise
                                if confidence > 0.40: 
                                    out.write(f"[{confidence:.2f}] {text}\n")
                                    text_blocks_found += 1
                                    
                            out.write("\n")
                            images_processed += 1
                            
                    except Exception as e:
                        print(colored(f"  [-] Inference error on {file}: {e}", "red"))

    if images_processed == 0:
         print(colored("\n[-] Triage complete. No valid images found or no text extracted.", "yellow"))
    else:
        print(colored(f"\n[✓] Vision Triage Complete.", "blue", attrs=["bold"]))
        print(f" [+] Images Processed: {images_processed}")
        print(f" [+] Text Blocks Extracted: {text_blocks_found}")
        print(colored(f"[*] Extraction log secured at: {output_log}", "green"))
        print("[*] Pivot Action: Run threat_intel_parser.py against this text log.")

if __name__ == "__main__":
    # Ensure a local directory named 'forensic_vault' exists with test images
    os.makedirs("forensic_vault", exist_ok=True)
    execute_vision_triage("forensic_vault")