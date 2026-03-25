import sys
import subprocess
import requests
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

def get_abstract_lead(description):
    print(colored("--- INITIATING ABSTRACTED GEOLOCATION REASONING ---", "blue", attrs=["bold"]))
    
    # Pre-structured prompt that turns the LLM into an OSINT expert
    system_prompt = (
        "You are an elite OSINT Geolocation Assistant. I will describe a photo to you.\n"
        "Your goal is to narrow down the Country and City using your database of global infrastructure.\n"
        "Pay attention to: power plug types, road line colors (yellow vs white), driver side, and architecture."
    )
    
    prompt = f"{system_prompt}\n\nDESCRIPTION: {description}\n\nWhat is the most likely location and why?"

    payload = {
        "model": "llama3", # Requirements: 'ollama pull llama3'
        "prompt": prompt,
        "stream": False
    }

    try:
        print(colored("[*] Querying local Llama3 brain...", "yellow"))
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)
        result = response.json()
        
        print(colored("\n[!] PROBABLE LOCATION LEAD:", "green", attrs=["bold"]))
        print(result.get("response", "No lead generated."))
        
    except Exception as e:
        print(colored(f"[-] Connection Error: {e}", "red"))

if __name__ == "__main__":
    print(colored("Enter the visual description (e.g., 'Yellow center lines, birch trees, Type G plugs'):", "cyan"))
    user_input = input("> ")
    get_abstract_lead(user_input)