#!/usr/bin/env python3
import numpy as np

def optimize_path(contours):
    if not contours:
        return contours

    optimized = []
    remaining = list(range(len(contours)))
    current_pos = (0.0, 0.0)

    while remaining:
        nearest_idx = None
        nearest_dist = float('inf')

        for idx in remaining:
            start = contours[idx][0]
            dist = np.sqrt((current_pos[0] - start[0])**2 +
                          (current_pos[1] - start[1])**2)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_idx = idx

        optimized.append(contours[nearest_idx])
        current_pos = contours[nearest_idx][-1]
        remaining.remove(nearest_idx)

    print(f"Path optimized — {len(optimized)} contours in optimal order")
    return optimized
