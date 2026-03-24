import sys
import subprocess
import os

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {'playwright': 'playwright', 'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
            # Playwright requires post-install binary downloading
            if pkg == 'playwright':
                print("[*] Installing Playwright Chromium binaries...")
                subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
ensure_deps()
# -------------------------------

from playwright.sync_api import sync_playwright
from termcolor import colored

def headless_breach(target_url):
    print(colored(f"--- INITIATING HEADLESS INFILTRATOR ---", "blue", attrs=["bold"]))
    print(f"[*] Target: {target_url}")
    print("[*] Spinning up invisible Chromium engine...")
    
    with sync_playwright() as p:
        # Launch browser. Set headless=False to watch the bot visually during testing.
        browser = p.chromium.launch(headless=True)
        
        # Spoof a standard civilian browser context
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True # Bypass bad SSL certs
        )
        
        page = context.new_page()
        
        try:
            print(colored("[*] Executing JavaScript evasion and waiting for DOM rendering...", "yellow"))
            # networkidle ensures all background JS and API calls have finished loading
            page.goto(target_url, wait_until="networkidle", timeout=30000)
            
            # Extract the fully rendered HTML
            rendered_html = page.content()
            page_title = page.title()
            
            print(colored(f"[✓] JS Execution Complete. Page Title: '{page_title}'", "green", attrs=["bold"]))
            
            # Secure the payload to the offline vault
            vault_dir = "forensic_vault"
            os.makedirs(vault_dir, exist_ok=True)
            file_path = os.path.join(vault_dir, "rendered_target.html")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(rendered_html)
                
            print(colored(f"[*] Rendered payload secured at: {file_path}", "blue"))
            print("[*] You may now process this file with stealth_scraper.py or tracking_id_pivot.py")
            
        except Exception as e:
            print(colored(f"[-] Headless breach failed: {e}", "red"))
            
        finally:
            browser.close()

if __name__ == "__main__":
    # Example Target: A site known to use heavy JS or Cloudflare challenges
    headless_breach("https://mock-investment-scam.com")