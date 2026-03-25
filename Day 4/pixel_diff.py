import cv2 # pip install opencv-python
import numpy as np

def detect_geoint_changes(img1_path, img2_path):
    print(colored("--- EXECUTING SATELLITE CHANGE DETECTION ---", "blue"))
    
    # Load images in grayscale
    before = cv2.imread(img1_path, 0)
    after = cv2.imread(img2_path, 0)

    # Calculate absolute difference between frames
    diff = cv2.absdiff(before, after)
    
    # Threshold to highlight significant changes (metal objects in SAR)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    cv2.imwrite("change_detected.png", thresh)
    print(colored("[✓] Change map generated: change_detected.png", "green"))

# Usage: detect_geoint_changes("site_monday.png", "site_thursday.png")