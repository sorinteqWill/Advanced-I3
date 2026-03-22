# run me after the target_archive.html file ahs been downlaoded
import sys
import subprocess

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {'requests': 'requests', 'beautifulsoup4': 'bs4', 'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
ensure_deps()
# -------------------------------

import os
import requests
from bs4 import BeautifulSoup
from termcolor import colored
from urllib.parse import urljoin
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_assets(base_url, html_file):
    print(colored("--- AUTOMATED ASSET EXTRACTION ---", "blue", attrs=["bold"]))
    
    # Create secure offline vault
    vault_dir = "forensic_vault"
    os.makedirs(vault_dir, exist_ok=True)
    
    try:
        with open(html_file, 'r', encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        # Look for links and image sources
        target_extensions = ('.pdf', '.docx', '.jpg', '.jpeg', '.png')
        assets_found = []
        
        for tag in soup.find_all(['a', 'img']):
            link = tag.get('href') or tag.get('src')
            if link and link.lower().endswith(target_extensions):
                full_url = urljoin(base_url, link)
                assets_found.append(full_url)
                
        # Deduplicate list
        assets_found = list(set(assets_found))
        print(colored(f"[*] Identified {len(assets_found)} high-value target assets.", "yellow"))
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        for asset_url in assets_found:
            file_name = asset_url.split('/')[-1]
            save_path = os.path.join(vault_dir, file_name)
            
            print(f" [+] Downloading: {file_name}...")
            response = requests.get(asset_url, headers=headers, verify=False, timeout=15)
            
            if response.status_code == 200:
                with open(save_path, 'wb') as asset_file:
                    asset_file.write(response.content)
            else:
                print(colored(f"  [-] Failed (HTTP {response.status_code})", "red"))
                
        print(colored(f"\n[✓] Asset extraction complete. Files secured in ./{vault_dir}/", "green"))
        
    except Exception as e:
        print(colored(f"[-] Asset Extraction Error: {e}", "red"))

if __name__ == "__main__":
    # Example Usage
    extract_assets("http://mock-investment-scam.com", "target_archive.html")
