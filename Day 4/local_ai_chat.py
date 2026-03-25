import sys
import subprocess
import requests
import json
import base64
import os
from termcolor import colored

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

def encode_image(image_path):
    """Converts a local image into a Base64 string for the AI model."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def local_ai_geolocate(image_path):
    print(colored("--- INITIATING LOCAL LLaVA VISUAL ANALYSIS ---", "blue", attrs=["bold"]))
    print(f"[*] Analyzing Image: {image_path}")
    
    # Tactical OSINT Prompt: Forces 'Chain-of-Thought' reasoning
    prompt = (
        "Perform a tactical OSINT analysis of this image. Follow these steps exactly:\n"
        "1. Identify and list all visible text, logos, or license plate formats.\n"
        "2. Describe unique architectural styles, vegetation (flora), and utility pole designs.\n"
        "3. Analyze the sun/shadows to estimate the cardinal direction the camera is facing.\n"
        "4. Based on the above, provide the most likely Country and City.\n"
        "5. Provide a Confidence Score (0-100%) and justify your uncertainty.\n"
        "DO NOT HALLUCINATE. If you cannot see a detail, state 'Unknown'."
    )

    payload = {
        "model": "llava", # Requirements: 'ollama pull llava' must be run on the Kali machine
        "prompt": prompt,
        "images": [encode_image(image_path)],
        "stream": False
    }

    try:
        print(colored("[*] Connecting to local Ollama API... (Data remains offline)", "yellow"))
        # Standard Ollama local port is 11434
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
        result = response.json()
        
        analysis = result.get("response", "No response from model.")
        
        print(colored("\n[!] TACTICAL VISUAL REPORT:", "green", attrs=["bold"]))
        print("-" * 50)
        print(analysis)
        print("-" * 50)
        
        # Save report to the vault
        report_path = "forensic_vault/ai_visual_analysis.txt"
        with open(report_path, "w") as f:
            f.write(f"IMAGE: {image_path}\n")
            f.write(analysis)
        print(colored(f"\n[*] Report secured to: {report_path}", "blue"))

    except requests.exceptions.ConnectionError:
        print(colored("[-] Error: Ollama is not running. Start it with 'ollama serve'.", "red"))
    except Exception as e:
        print(colored(f"[-] AI Analysis Error: {e}", "red"))

if __name__ == "__main__":
    # Ensure the directory exists
    os.makedirs("forensic_vault", exist_ok=True)
    target = "forensic_vault/target_photo.jpg"
    
    if os.path.exists(target):
        local_ai_geolocate(target)
    else:
        print(colored(f"[-] Please place an image at {target} to test.", "yellow"))