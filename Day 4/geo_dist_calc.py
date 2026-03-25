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

import math
from termcolor import colored

def calculate_haversine(lat1, lon1, lat2, lon2):
    print(colored(f"--- GEOGRAPHIC DISTANCE CALCULATOR ---", "blue", attrs=["bold"]))
    
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance_km = R * c
    distance_meters = distance_km * 1000
    
    print(colored(f"\n[!] PROXIMITY ANALYSIS COMPLETE:", "green", attrs=["bold"]))
    print(f" [+] Distance (KM): {distance_km:.4f} km")
    print(f" [+] Distance (Meters): {distance_meters:.2f} m")
    
    if distance_meters < 50:
        print(colored("[!] ALERT: High-proximity overlap detected (<50m). Potential physical meeting.", "red", attrs=["blink"]))

    return distance_km

if __name__ == "__main__":
    # Example: Point A (London Eye) and Point B (Big Ben)
    calculate_haversine(51.5033, -0.1195, 51.5007, -0.1246)