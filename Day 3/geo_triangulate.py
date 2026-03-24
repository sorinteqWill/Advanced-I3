import math
from termcolor import colored

def calculate_intersection(p1, p2, p3, d1, d2, d3):
    """
    p1, p2, p3 are (x, y) coordinates of your 3 spoofed locations.
    d1, d2, d3 are the distances Telegram reports for the suspect.
    """
    print(colored("--- CALCULATING SUSPECT INTERSECTION ---", "blue", attrs=["bold"]))
    
    # Simple 2D trilateration formula
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2

    try:
        x = (C*E - F*B) / (E*A - B*D)
        y = (A*F - D*C) / (A*E - B*D)
        
        print(colored(f"[!] Target Pinpointed!", "green"))
        print(f"[+] Estimated Lat: {x}")
        print(f"[+] Estimated Lon: {y}")
        print(f"[*] Drop these coordinates into Google Maps for the physical raid.")
    except ZeroDivisionError:
        print(colored("[-] Calculation Error: Points are collinear.", "red"))

# Example Usage: 
# loc1 = (51.5074, 0.1278) # London Eye
# loc2 = (51.5014, 0.1419) # Buckingham Palace
# loc3 = (51.4994, 0.1273) # Westminster
# calculate_intersection(loc1, loc2, loc3, 800, 1200, 500)