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
import json
import csv
import time
from termcolor import colored
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# OPERATOR CONFIGURATION REQUIRED
UCO_TOKEN = 'your_extracted_discord_authorization_token_here'
# ==========================================

def archive_discord_channel(channel_id, max_requests=10):
    print(colored(f"--- INITIATING DISCORD API INFILTRATOR ---", "blue", attrs=["bold"]))
    print(f"[*] Target Channel ID: {channel_id}")
    
    headers = {
        'Authorization': UCO_TOKEN,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/json'
    }
    
    base_url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100"
    
    output_file = f"Discord_Archive_{channel_id}.csv"
    last_message_id = None
    total_messages = 0
    
    print(colored(f"[*] Commencing asynchronous extraction to {output_file}...", "yellow"))
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Message_ID', 'Timestamp', 'Author', 'Content', 'Attachments'])
        
        for request_count in range(max_requests):
            target_url = base_url
            if last_message_id:
                target_url += f"&before={last_message_id}"
                
            try:
                response = requests.get(target_url, headers=headers, timeout=15, verify=False)
                
                if response.status_code == 200:
                    messages = response.json()
                    if not messages:
                        print(colored("[*] Reached the beginning of the channel history.", "green"))
                        break
                        
                    for msg in messages:
                        msg_id = msg.get('id')
                        timestamp = msg.get('timestamp')
                        author = msg.get('author', {}).get('username', 'Unknown')
                        content = msg.get('content', '').replace('\n', ' ')
                        
                        # Extract attachment URLs
                        attachments = [att.get('url') for att in msg.get('attachments', [])]
                        att_string = " | ".join(attachments) if attachments else "None"
                        
                        writer.writerow([msg_id, timestamp, author, content, att_string])
                        last_message_id = msg_id # Set for the next pagination loop
                        total_messages += 1
                        
                    print(f" [+] Extracted batch {request_count + 1} ({len(messages)} messages).")
                    time.sleep(1.5) # Critical anti-ban delay
                    
                elif response.status_code == 401:
                    print(colored("[-] Critical Error: UCO Token is invalid or expired.", "red"))
                    break
                elif response.status_code == 429:
                    print(colored("[-] Rate Limited by Discord API. Waiting 5 seconds...", "yellow"))
                    time.sleep(5)
                else:
                    print(colored(f"[-] API Error {response.status_code}: {response.text}", "red"))
                    break
                    
            except Exception as e:
                print(colored(f"[-] Connection failed: {e}", "red"))
                break

    print(colored(f"\n[✓] Infiltration Complete. {total_messages} messages secured.", "blue", attrs=["bold"]))

if __name__ == "__main__":
    # Example target: A hypothetical channel ID
    # You must enable Developer Mode in Discord settings, right-click a channel, and "Copy ID"
    target_channel = "123456789012345678" 
    
    if UCO_TOKEN == 'your_extracted_discord_authorization_token_here':
        print(colored("[-] STOP: You must insert your extracted UCO_TOKEN into the script.", "red"))
    else:
        archive_discord_channel(target_channel, max_requests=5)