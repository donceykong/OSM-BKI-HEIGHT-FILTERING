#!/usr/bin/env python3
"""
Plot the example lidar GPS track (poses) on an interactive map using folium.

Loads lidar_gps.csv (num, lat, lon) for a given dataset and sequence and draws the drive path on OSM tiles.
No separate OSM file is loaded—only the built-in map tiles and the track :)

Usage:
  python plot_gps_on_folium.py --dataset mcd --sequence kth_day_09
  python plot_gps_on_folium.py --dataset kitti360 --sequence 2013_05_28_drive_0000_sync
"""

import argparse
import os
import sys
import pandas as pd
import folium


def load_gps_track(csv_path):
    """Load lidar_gps.csv. Returns list of (lat, lon) or None on failure."""
    if not os.path.isfile(csv_path):
        return None
    df = pd.read_csv(csv_path)
    if "lat" not in df.columns or "lon" not in df.columns:
        return None
    df = df.sort_values("num")
    return list(zip(df["lat"].astype(float), df["lon"].astype(float)))


def build_map(gps_track, center_lat, center_lon):
    """Build a folium Map with GPS track (black line, green start, red end)."""
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=16,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    if gps_track and len(gps_track) >= 2:
        folium.PolyLine(
            gps_track,
            color="black",
            weight=4,
            opacity=0.9,
            popup="LiDAR poses",
        ).add_to(m)
        folium.CircleMarker(
            gps_track[0],
            radius=6,
            color="green",
            fill=True,
            fillColor="green",
            popup="Start",
        ).add_to(m)
        folium.CircleMarker(
            gps_track[-1],
            radius=6,
            color="darkred",
            fill=True,
            fillColor="red",
            popup="End",
        ).add_to(m)

    return m


def main():
    parser = argparse.ArgumentParser(
        description="Plot data GPS track on an interactive map (folium).",
    )
    parser.add_argument(
        "--dataset-path",
        type=str,
        required=False,
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_samples"),
        help="Path to the dataset",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        choices=["mcd", "kitti360"],
        help="Dataset name",
    )
    parser.add_argument(
        "--sequence",
        type=str,
        required=True,
        help="Sequence name (e.g. kth_day_09 or 2013_05_28_drive_0000_sync)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output HTML path (default: data/<dataset>/<sequence>/gps_on_osm.html)",
    )
    args = parser.parse_args()

    # Get ze necessary data
    gps_path = os.path.join(args.dataset_path, args.dataset, args.sequence, "lidar_gps.csv")
    gps_track = load_gps_track(gps_path)

    # For ensuring the view is centered on the lidar GPS track
    center_lat = sum(p[0] for p in gps_track) / len(gps_track)
    center_lon = sum(p[1] for p in gps_track) / len(gps_track)

    m = build_map(gps_track, center_lat, center_lon)

    if args.output:
        out_path = args.output
    else:
        seq_dir = os.path.join(args.dataset_path, args.dataset, args.sequence)
        out_path = os.path.join(seq_dir, "gps_on_osm.html")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    m.save(out_path)
    print(f"Saved map to {out_path}")
    print(f"  GPS points: {len(gps_track)}")


if __name__ == "__main__":
    main()
