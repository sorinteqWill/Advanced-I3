import os
import random
import time

def generate_massive_log():
    filename = "apache_seized.log"
    print(f"[*] Generating massive seized log file: {filename}...")
    
    # We will generate about 5 million lines (roughly 500MB - 1GB)
    total_lines = 5000000
    needle_line = 3456789 # Bury it deep
    
    with open(filename, "w") as f:
        for i in range(total_lines):
            if i == needle_line:
                # The Golden Artifact
                f.write('192.168.1.55 - - [17/Mar/2026:23:15:00 +0000] "POST /login?user=Admin_Phantom HTTP/1.1" 200 4322 "-" "Mozilla/5.0"\n')
            else:
                # Junk Noise
                fake_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                f.write(f'{fake_ip} - - [17/Mar/2026:10:00:00 +0000] "GET /wp-login.php HTTP/1.1" 401 543 "-" "Bot/1.0"\n')
                
            if i % 500000 == 0 and i > 0:
                print(f" [+] Generated {i} lines...")
                
    print(f"[✓] Log generation complete. File size: {os.path.getsize(filename) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    generate_massive_log()