import exiftool # Requires: pip install pyexiftool
import random

def sanitize_and_inject(image_path, target_lat, target_lon):
    # Standard hardware profiles for spoofing
    hardware_profiles = [
        {"Make": "Apple", "Model": "iPhone 14 Pro", "Software": "iOS 17.1"},
        {"Make": "Samsung", "Model": "SM-S928B", "Software": "Android 14"}
    ]
    
    profile = random.choice(hardware_profiles)
    
    with exiftool.ExifToolHelper() as et:
        print(f"[+] Scrubbing all existing metadata from {image_path}...")
        # Strip everything first to remove AI signatures
        et.execute("-all=", image_path)
        
        print(f"[+] Injecting {profile['Model']} profile and GPS coordinates...")
        # Inject realistic hardware and location signatures
        et.set_tags(
            [image_path],
            tags={
                "Make": profile["Make"],
                "Model": profile["Model"],
                "Software": profile["Software"],
                "GPSLatitude": target_lat,
                "GPSLongitude": target_lon,
                "GPSLatitudeRef": "N",
                "GPSLongitudeRef": "W",
                "DateTimeOriginal": "2026:03:10 14:22:01"
            },
            params=["-overwrite_original"]
        )
    print(colored("[✓] Identity Anchor Sealed.", "green"))

# Example Usage: Sanitize a face and place it in Central London
# sanitize_and_inject("persona_face.jpg", 51.5074, 0.1278)