# OSM-BKI HEIGHT-FILTERING

Plot the example KITTI-360 or MCD lidar GPS-based pose tracks on an interactive map. You can Zoom in or out as you need to geolocate when trying to find overlapping .las DSM and .tif DEM files.

**How to run** (from this folder):

```bash
# MCD
python plot_gps_on_folium.py --dataset mcd --sequence kth_day_09

# KITTI-360
python plot_gps_on_folium.py --dataset kitti360 --sequence 2013_05_28_drive_0000_sync
```

Uses `data_samples/` by default. Add `--dataset-path /path/to/data` to use your own data. Output: `gps_on_osm.html` in the sequence folder.

---