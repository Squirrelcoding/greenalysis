from rasterio.windows import Window
from rasterio.transform import rowcol
import numpy as np

ACRE_EDGE_METERS = 500
DEGREES_PER_METER = 8.983e-6

def generate_point(raster):
    lat = np.random.uniform(
        raster.bounds.bottom + ACRE_EDGE_METERS * DEGREES_PER_METER, 
        raster.bounds.top
    )

    lon = np.random.uniform(
        raster.bounds.left, 
        raster.bounds.right - ACRE_EDGE_METERS * DEGREES_PER_METER
    )
    return lat, lon

def generate_window(region, from_wsg84, lon, lat):
    x, y = from_wsg84.transform(lon, lat)
    row_min, col_min = rowcol(region.transform, x, y)

    # Bottom right for green
    x, y = from_wsg84.transform(lon + ACRE_EDGE_METERS * DEGREES_PER_METER, lat - ACRE_EDGE_METERS * DEGREES_PER_METER)
    row_max, col_max = rowcol(region.transform, x, y)
    window = Window(col_off=col_min, row_off=row_min, width=col_max-col_min+1, height=row_max-row_min+1)

    return window