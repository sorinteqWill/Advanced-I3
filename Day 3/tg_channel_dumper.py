import sys
import subprocess

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {'telethon': 'telethon', 'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
ensure_deps()
# -------------------------------

from telethon.sync import TelegramClient
import csv
from termcolor import colored

# ==========================================
# OPERATOR CONFIGURATION REQUIRED
# Get these from https://my.telegram.org
API_ID = '1234567'  # Replace with your integer ID
API_HASH = 'your_32_char_api_hash_here'
PHONE_NUMBER = '+1234567890' # Replace with UCO Burner Number
# ==========================================

def dump_telegram_channel(target_channel, message_limit=100):
    print(colored(f"--- INITIATING TELEGRAM MTPROTO ARCHIVER ---", "blue", attrs=["bold"]))
    print(f"[*] Target Entity: {target_url}")
    print("[*] Authenticating Undercover Session...")
    
    # Initialize the client. The first parameter creates 'UCO_Session.session' locally.
    client = TelegramClient('UCO_Session', API_ID, API_HASH)
    
    try:
        # start() handles the SMS verification if the session file doesn't exist
        client.start(phone=PHONE_NUMBER)
        print(colored("[✓] UCO Authentication Successful.", "green"))
        
        output_file = f"TG_Archive_{target_channel.replace('@', '')}.csv"
        print(colored(f"[*] Commencing data extraction (Limit: {message_limit} messages)...", "yellow"))
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Message_ID', 'Timestamp_UTC', 'Sender_ID', 'Message_Text'])
            
            msg_count = 0
            # iter_messages pulls chronologically (newest first)
            for message in client.iter_messages(target_channel, limit=message_limit):
                if message.text: # Only log messages containing actual text
                    # Format timestamp
                    msg_date = message.date.strftime('%Y-%m-%d %H:%M:%S')
                    sender = message.sender_id or "Anonymous/Channel"
                    
                    # Clean newlines from the message text to prevent CSV corruption
                    clean_text = message.text.replace('\n', ' ').replace('\r', '')
                    
                    writer.writerow([message.id, msg_date, sender, clean_text])
                    msg_count += 1
                    
        print(colored(f"\n[✓] Extraction Complete. {msg_count} records secured in {output_file}", "blue", attrs=["bold"]))

    except Exception as e:
        print(colored(f"[-] Telegram API Error: {e}", "red"))
        print("[*] Verify API credentials and ensure the target channel exists.")
        
    finally:
        client.disconnect()

if __name__ == "__main__":
    # Example Target: A public Telegram channel handle
    target_url = "@telegram" # Using the official Telegram channel as a safe test
    
    # SAFETY CHECK
    if API_ID == '1234567':
        print(colored("[-] STOP: You must input your API_ID and API_HASH into the script.", "red"))
    else:
        dump_telegram_channel(target_url, message_limit=50)