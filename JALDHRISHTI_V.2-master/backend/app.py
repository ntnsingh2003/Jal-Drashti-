#!/usr/bin/env python3
"""
Jal Drishti - Backend Demonstration
====================================
Demonstrates the core AI algorithms for flood risk assessment and resource optimization.
"""

import sys

import numpy as np

from backend.services.rescue_path_finder import RescuePathFinder
from backend.services.resource_allocator import ResourceAllocator


def safe_print(message=""):
    """Print without crashing on terminals that do not support Unicode output."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        print(message)
    except UnicodeEncodeError:
        sanitized = str(message).encode(encoding, errors="replace").decode(encoding)
        print(sanitized)


def demo_rescue_path():
    """Demonstrate path finding between locations."""
    safe_print("Rescue Path Finding Demo")
    safe_print("=" * 40)

    pf = RescuePathFinder()
    start = (11.2588, 75.7804)
    end = (11.2600, 75.7850)

    result = pf.find_path(start, end)
    safe_print(f"Start: {start}")
    safe_print(f"End: {end}")
    safe_print(f"Distance: {result['statistics']['distance_m']:.1f} meters")
    safe_print(f"Travel Time: {result['statistics']['time_min']:.1f} minutes")
    safe_print()


def demo_resource_allocation():
    """Demonstrate resource allocation across affected areas."""
    safe_print("Resource Allocation Demo")
    safe_print("=" * 40)

    centers = [
        (11.2588, 75.7804),
        (11.2700, 75.7900),
    ]
    clusters = [
        {"lat": 11.2600, "lng": 75.7820, "population": 500, "cluster_id": 1},
        {"lat": 11.2650, "lng": 75.7850, "population": 300, "cluster_id": 2},
        {"lat": 11.2750, "lng": 75.7950, "population": 800, "cluster_id": 3},
    ]

    pf = RescuePathFinder()
    allocator = ResourceAllocator(centers, clusters, pf)
    result = allocator.allocate_resources(2)

    safe_print(f"Allocating 2 ambulances across {len(clusters)} clusters")
    safe_print(f"Assignments: {result['assignments']}")
    safe_print(f"Max Response Time: {result['max_response_time']:.1f} minutes")
    safe_print(f"Avg Response Time: {result['avg_response_time']:.1f} minutes")
    safe_print(f"Population Covered: {result['coverage_population']}")
    safe_print()


def demo_flood_risk():
    """Demonstrate flood risk classification."""
    safe_print("Flood Risk Classification Demo")
    safe_print("=" * 40)

    def classify_risk(water_depth, elevation):
        depth_score = min(100, (water_depth / 4) * 100) * 0.40
        slope_score = max(0, 100 - (elevation / 20) * 100) * 0.25
        accum_score = min(100, water_depth * 25) * 0.25
        total = depth_score + slope_score + accum_score + 50 * 0.10

        if total >= 90:
            return "extreme"
        if total >= 70:
            return "high"
        if total >= 50:
            return "medium"
        return "low"

    test_cases = [(0.5, 100), (2.0, 50), (4.0, 10)]
    for depth, elev in test_cases:
        risk = classify_risk(depth, elev)
        safe_print(f"Water Depth: {depth}m, Elevation: {elev}m -> Risk: {risk.upper()}")


if __name__ == "__main__":
    safe_print("Jal Drishti - AI-Driven Flood Intelligence Backend Demo")
    safe_print("=" * 60)
    safe_print()
    demo_rescue_path()
    demo_resource_allocation()
    demo_flood_risk()
    safe_print("All demos completed successfully.")
    safe_print("\nTo run the frontend dashboard:")
    safe_print("  python -m http.server 8001")
    safe_print("  Open: http://localhost:8001/frontend")
