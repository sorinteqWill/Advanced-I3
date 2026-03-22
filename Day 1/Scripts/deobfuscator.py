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

import base64
import urllib.parse
import binascii
from termcolor import colored

def attempt_decoding(obfuscated_string):
    print(colored("--- PAYLOAD DEOBFUSCATION ENGINE ---", "blue", attrs=["bold"]))
    print(f"[*] Analyzing Target String: {obfuscated_string[:30]}...\n")
    
    # 1. Base64 Decoding
    try:
        # Pad string if necessary
        padded_str = obfuscated_string + '=' * (-len(obfuscated_string) % 4)
        b64_decoded = base64.b64decode(padded_str).decode('utf-8')
        print(colored(f"[✓] Base64 Decode Match: {b64_decoded}", "green"))
    except Exception:
        print(colored("[-] Not valid Base64.", "yellow"))

    # 2. URL Decoding
    try:
        url_decoded = urllib.parse.unquote(obfuscated_string)
        if url_decoded != obfuscated_string:
            print(colored(f"[✓] URL Decode Match: {url_decoded}", "green"))
        else:
            print(colored("[-] Not URL Encoded.", "yellow"))
    except Exception:
        pass

    # 3. Hex Decoding
    try:
        clean_hex = obfuscated_string.replace('0x', '').replace(' ', '')
        hex_decoded = binascii.unhexlify(clean_hex).decode('utf-8')
        print(colored(f"[✓] Hex Decode Match: {hex_decoded}", "green"))
    except Exception:
        print(colored("[-] Not valid Hexadecimal.", "yellow"))

if __name__ == "__main__":
    # Example Usage: A Base64 encoded Google Tag Manager ID
    suspicious_payload = "R1RNLVg5OEIyTA=="
    attempt_decoding(suspicious_payload)