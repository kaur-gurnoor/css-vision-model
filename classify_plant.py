# Generative AI was used to help debugg this code

import cv2
import numpy as np
import sys
from pathlib import Path

def analyze_image(image_path: str):
    image_path = Path(image_path)
    img = cv2.imread(str(image_path))
    img_resized = cv2.resize(img, (400, 400))
    hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    lower_yellow = np.array([20, 40, 40])
    upper_yellow = np.array([35, 255, 255])
    lower_brown = np.array([0, 40, 0])
    upper_brown = np.array([30, 255, 120])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    total_pixels = hsv.shape[0] * hsv.shape[1]
    green_pct = np.sum(mask_green > 0) / total_pixels * 100
    yellow_pct = np.sum(mask_yellow > 0) / total_pixels * 100
    brown_pct = np.sum(mask_brown > 0) / total_pixels * 100
    print(f"\nAnalysis for {image_path.name}:")
    print(f"  Green:  {green_pct:.1f}%")
    print(f"  Yellow: {yellow_pct:.1f}%")
    print(f"  Brown:  {brown_pct:.1f}%")
    if green_pct > 50 and yellow_pct < 15 and brown_pct < 10:
        status = "HEALTHY"
    elif yellow_pct >= 15 and yellow_pct >= brown_pct:
        status = "YELLOWING"
    elif brown_pct >= 15:
        status = "STRESSED_DARK_OR_WILTED"
    else:
        status = "UNCERTAIN"
    print(f"  Status: {status}")
    action = decide_action(status)
    print(f"  Suggested action: {action}\n")
def decide_action(status: str) -> str:
    if status == "HEALTHY":
        return "No change. Keep current nutrient and light settings stable."
    if status == "YELLOWING":
        return "Increase nutrient concentration slightly in this zone and verify pH is within target range."
    if status == "STRESSED_DARK_OR_WILTED":
        return "Check water delivery and increase light duration or intensity slightly in this zone."
    return "Flag for manual review. Pattern does not clearly match stored conditions."
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py classify_plant.py path/to/image.png")
    else:
        analyze_image(sys.argv[1])

