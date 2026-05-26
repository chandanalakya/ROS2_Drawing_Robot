#!/usr/bin/env python3
import cv2
import numpy as np

def process_image(image_path, canvas_size=0.4):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not load image from {image_path}")
        return []

    # Resize to square
    img = cv2.resize(img, (500, 500))

    # Show what we loaded (for debugging)
    print(f"Image size: {img.shape}")

    # Blur slightly
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Threshold — works better than Canny for simple drawings
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # Find ALL contours including inner ones (eyes, smile)
    contours, hierarchy = cv2.findContours(
        thresh,
        cv2.RETR_TREE,          # Gets ALL contours including holes
        cv2.CHAIN_APPROX_NONE   # Keep ALL points for accuracy
    )

    if hierarchy is None:
        print("No contours found!")
        return []

    # Sort by area — largest first
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    waypoints = []
    for contour in contours:
        area = cv2.contourArea(contour)

        # Skip tiny noise but allow small features like eyes
        if area < 3:
            continue

        contour_points = []
        for point in contour:
            px, py = point[0]

            # Normalize to robot range
            x = (px / 500.0 - 0.5) * canvas_size

            # FLIP Y axis — OpenCV Y is top-down, RViz Y is bottom-up
            y = -(py / 500.0 - 0.5) * canvas_size

            contour_points.append((x, y))

        # Close the contour by returning to start point
        if len(contour_points) > 0:
            contour_points.append(contour_points[0])

        waypoints.append(contour_points)

    print(f"Found {len(waypoints)} contours")
    for i, wp in enumerate(waypoints):
        print(f"  Contour {i+1}: {len(wp)} points, area={cv2.contourArea(contours[i]):.1f}")

    return waypoints

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 image_processor.py <image_path>")
    else:
        waypoints = process_image(sys.argv[1])
