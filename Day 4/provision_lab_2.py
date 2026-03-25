import os
import random
from termcolor import colored

def create_lab_environment():
    print(colored("--- PROVISIONING LAB 2: OPERATION ASSOCIATE HUNT ---", "blue", attrs=["bold"]))
    
    # Create the directory
    folder = "lab_data"
    os.makedirs(folder, exist_ok=True)
    
    # Common "Noise" usernames (Bots, celebrities, etc.)
    noise = ["elonmusk", "realdonaldtrump", "cz_binance", "vitalik.eth", "official_nasa", "bot_992", "spam_tracker"]
    
    # Criminal Associates for Suspect A
    associates_a = [f"user_{random.randint(1000, 9999)}" for _ in range(450)]
    
    # Criminal Associates for Suspect B
    associates_b = [f"shadow_{random.randint(1000, 9999)}" for _ in range(450)]
    
    # The "Hidden Mutuals" (The targets)
    # 1. The Gatekeeper (High Value)
    # 2. A known low-level mule
    # 3. An accidental mutual (The "Noise" celebrity)
    mutuals = ["crypto_cleaner_uk", "mule_operator_01", "cz_binance"]
    
    # Build Suspect A File
    list_a = associates_a + mutuals + noise
    random.shuffle(list_a)
    with open(os.path.join(folder, "suspect_a.txt"), "w") as f:
        f.write("\n".join(list_a))
        
    # Build Suspect B File
    list_b = associates_b + mutuals + noise
    random.shuffle(list_b)
    with open(os.path.join(folder, "suspect_b.txt"), "w") as f:
        f.write("\n".join(list_b))
        
    print(colored(f"[✓] Lab data generated in ./{folder}/", "green"))
    print(f" [*] Created suspect_a.txt ({len(list_a)} entries)")
    print(f" [*] Created suspect_b.txt ({len(list_b)} entries)")
    print(colored("\n[!] INSTRUCTOR NOTE: The Gatekeeper is 'crypto_cleaner_uk'", "yellow"))

if __name__ == "__main__":
    create_lab_environment()