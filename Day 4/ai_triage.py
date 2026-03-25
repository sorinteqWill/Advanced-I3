import requests
import json
import csv

def extract_intel_with_ai(chat_log_path):
    print(f"[+] Feeding logs to local AI for triage...")
    
    with open(chat_log_path, 'r') as f:
        content = f.read()

    # Master prompt for the local model
    prompt = f"""
    Act as a Law Enforcement Intelligence Analyst. 
    Extract all 'Account Numbers', 'Sort Codes', 'IBANs', and 'Crypto Wallets' from the following text.
    Output the results as a raw JSON list only.
    Text: {content}
    """

    # Connect to local Ollama API
    response = requests.post("http://localhost:11434/api/generate", 
                             json={"model": "llama3", "prompt": prompt, "stream": False})
    
    entities = json.loads(response.json()['response'])
    print(colored(f"[!] AI Extracted {len(entities)} high-value targets.", "green"))
    # Logic to save to CSV here...

# Usage: extract_intel_with_ai("manchester_meds_logs.txt")