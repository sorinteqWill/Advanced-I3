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

def calculate_solar_altitude(object_height, shadow_length, unit="Meters"):
    print(colored(f"--- MATHEMATICAL CHRONOLOCATION ENGINE ---", "blue", attrs=["bold"]))
    print(f"[*] Known Object Height: {object_height} {unit}")
    print(f"[*] Measured Shadow Length: {shadow_length} {unit}")
    
    if shadow_length <= 0:
        print(colored("[!] Shadow length is zero. The sun is directly overhead (90.0 degrees).", "yellow"))
        return 90.0
    if object_height <= 0:
        print(colored("[-] Error: Object height must be greater than zero.", "red"))
        return None

    # Calculate the angle using Inverse Tangent (Arctangent)
    # Theta = arctan(height / shadow_length)
    angle_radians = math.atan(object_height / shadow_length)
    
    # Convert radians to human-readable degrees
    angle_degrees = math.degrees(angle_radians)
    
    print(colored(f"\n[!] INTELLIGENCE EXTRACTED:", "green", attrs=["bold"]))
    print(f" [+] Solar Altitude Angle: {angle_degrees:.2f}°")
    
    print(colored("\n[*] Pivot Action: Input this angle and the photo's date/location into SunCalc.org", "cyan"))
    print("[*] Note: This calculation assumes a flat, level surface (0° incline).")
    
    return angle_degrees

if __name__ == "__main__":
    # Example Target: A 2.5-meter street sign casting a 3.8-meter shadow
    # Units do not matter as long as they are identical (e.g., both meters, or both pixels)
    h = 2.5
    s = 3.8
    calculate_solar_altitude(h, s, unit="Meters")