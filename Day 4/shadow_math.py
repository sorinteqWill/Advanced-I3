import math
from termcolor import colored

def calculate_solar_angles(object_height, shadow_length, shadow_azimuth_deg):
    print(colored("--- CALCULATING ASTROPHYSICAL TIME DATA ---", "blue", attrs=["bold"]))
    
    # Elevation Angle = arctan(height / length)
    elevation_rad = math.atan(object_height / shadow_length)
    elevation_deg = math.degrees(elevation_rad)
    
    # Solar Azimuth is always 180 degrees opposite the shadow
    solar_azimuth = (shadow_azimuth_deg + 180) % 360
    
    print(f"[+] Calculated Solar Elevation: {round(elevation_deg, 2)}°")
    print(f"[+] Calculated Solar Azimuth: {round(solar_azimuth, 2)}°")
    print(colored(f"[*] Input these into SunCalc.org to find the exact minute.", "yellow"))

# Example: A 2-meter signpost casts a 3.5-meter shadow pointing at 45° (NE)
# calculate_solar_angles(2, 3.5, 45)