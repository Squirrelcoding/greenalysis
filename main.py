import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.windows import from_bounds
from pyproj import Transformer

# downtown bbox in lat/lon (minx, miny, maxx, maxy)
downtown_latlon = (-93.285, 44.96, -93.25, 44.99)

# transformer from WGS84 -> UTM Zone 15N
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32615", always_xy=True)

# transform each corner
minx, miny = transformer.transform(downtown_latlon[0], downtown_latlon[1])
maxx, maxy = transformer.transform(downtown_latlon[2], downtown_latlon[3])

downtown_utm = (minx, miny, maxx, maxy)
print("Downtown bbox in UTM:", downtown_utm)


# Replace extreme values / NoData with np.nan
# You can check what the NoData value is from the raster profile
with rasterio.open("output.tif") as src:
    nodata = src.nodata
    window = from_bounds(*downtown_utm, src.transform)
    downtown_data = src.read(1, window=window)

# Mask NoData values
if nodata is not None:
    downtown_data = np.where(downtown_data == nodata, np.nan, downtown_data)

# Or clip extreme values if you don’t know nodata
downtown_data = np.clip(downtown_data, -50, 50)  # temperatures in Celsius, adjust as needed

# Plot
plt.imshow(downtown_data, cmap="inferno")
plt.colorbar(label="Temperature")
plt.title("Downtown Minneapolis Heatmap")
plt.show()
