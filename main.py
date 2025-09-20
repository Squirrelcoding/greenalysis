import rasterio
from rasterio.transform import rowcol
from pyproj import Transformer
import numpy as np

from generate_points import generate_point, generate_window

hennepin = rasterio.open("data/hennepin.tif")
green = rasterio.open("data/3.tif")

print(hennepin.meta)

h_to_wgs84 = Transformer.from_crs(hennepin.crs, "EPSG:4326", always_xy=True)
h_from_wgs84 = Transformer.from_crs("EPSG:4326", hennepin.crs, always_xy=True)

g_to_wgs84 = Transformer.from_crs(green.crs, "EPSG:4326", always_xy=True)
g_from_wgs84 = Transformer.from_crs("EPSG:4326", green.crs, always_xy=True)

h_band = hennepin.read(1)
g_band = green.read(1)

data = {
    "heat": [],
    "green": [],
    "lat": [],
    "lon": []
}

vals = 0

while vals < 1_000:
    
    # Generate random coordinates
    lat, lon = generate_point(green)

    # Get windows
    green_window = generate_window(green, g_from_wgs84, lon, lat)
    heat_window = generate_window(hennepin, h_from_wgs84, lon, lat)

    green_data = green.read(1, window=green_window)
    heat_data = hennepin.read(1, window=heat_window)
    heat_data = np.nan_to_num(heat_data, nan=0.0, posinf=0.0, neginf=0.0)

    if not (np.isfinite(heat_data.sum()) and np.isfinite(green_data.sum())):
        print("GOT ILLEGAL VALUE")
        continue
    print("Here!")
    vals += 1
    data["heat"].append(heat_data.sum())
    data["green"].append(green_data.sum())
    data["lat"].append(lat)
    data["lon"].append(lon)