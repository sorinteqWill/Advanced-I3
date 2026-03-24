import sys
import subprocess

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {'playwright': 'playwright', 'termcolor': 'termcolor'}
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
ensure_deps()
# -------------------------------

from playwright.sync_api import sync_playwright
import time
import random
from termcolor import colored

def automate_liveliness(profile_name):
    print(colored(f"--- INITIATING AUTOMATED PERSONA LIVELINESS ---", "blue", attrs=["bold"]))
    print(f"[*] Loading Persistent UCO Profile: {profile_name}")
    
    benign_sites = [
        "https://en.wikipedia.org/wiki/Special:Random",
        "https://www.bbc.com/news",
        "https://www.theverge.com",
        "https://news.ycombinator.com/"
    ]
    
    with sync_playwright() as p:
        print(colored("[*] Launching Chromium (Headless)...", "yellow"))
        # Using a persistent context saves cookies, cache, and local storage to the disk
        context = p.chromium.launch_persistent_context(
            user_data_dir=f"./{profile_name}_data",
            headless=True, # Set to False if you want to watch the bot work
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        # Determine how many sites the persona will "visit" today
        sites_to_visit = random.randint(2, 4)
        targets = random.sample(benign_sites, sites_to_visit)
        
        for site in targets:
            try:
                print(f"\n[*] Persona navigating to: {site}")
                page.goto(site, wait_until="domcontentloaded", timeout=30000)
                
                # Simulate initial reading delay
                time.sleep(random.uniform(2.0, 5.0))
                
                # Simulate human scrolling
                scroll_steps = random.randint(3, 7)
                for _ in range(scroll_steps):
                    scroll_amount = random.randint(300, 800)
                    print(f" [+] Simulating scroll down ({scroll_amount}px)...")
                    page.mouse.wheel(0, scroll_amount)
                    
                    # Random chaotic mouse movements while reading
                    x = random.randint(100, 1800)
                    y = random.randint(100, 900)
                    page.mouse.move(x, y, steps=10) # 'steps' makes the movement gradual
                    
                    time.sleep(random.uniform(1.5, 4.0)) # Pause to "read"
                
                # Try to click a random link to deepen the history
                print(" [+] Attempting to click a random internal article...")
                links = page.locator("a").all()
                if links:
                    random_link = random.choice(links)
                    # Force click bypasses overlapping elements
                    random_link.click(force=True, timeout=5000)
                    page.wait_for_load_state("domcontentloaded", timeout=10000)
                    time.sleep(random.uniform(3.0, 6.0))
                    
                print(colored(f"[✓] Site interaction complete.", "green"))
                
            except Exception as e:
                print(colored(f"[-] Interaction skipped/failed: {e}", "yellow"))
                
        print(colored(f"\n[!] Liveliness cycle complete. Cookies and history saved to ./{profile_name}_data", "blue", attrs=["bold"]))
        context.close()

if __name__ == "__main__":
    # Example Usage: Run this daily via a cron job
    automate_liveliness("UCO_Alpha_Profile")