import rasterio
from rasterio.mask import mask
import geopandas as gpd

# Input data
polypath = "jabodetabek_admin_wokepseribu.geojson"
rasterpath = "jabodetabek_10prec.tiff"

# VECTOR
polygon_data = gpd.read_file(polypath)
# Transform into EPSG:4326, comment out if you use other CRS
if polygon_data.crs != "EPSG:4326":
    polygon_data = polygon_data.to_crs("EPSG:4326")

# RASTER
with rasterio.open(rasterpath) as src:
    # Masking the raster with the polygon
    out_image, out_transform = mask(src, polygon_data.geometry, crop=True, all_touched=True, invert=False)
    
    # Update the metadata
    out_meta = src.meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform,
        "nodata": src.nodata
    })

# Saving
maskedrasterpath = "masked_raster.tif"
with rasterio.open(maskedrasterpath, "w", **out_meta) as dest:
    dest.write(out_image)
    
print("Saved to:", maskedrasterpath)
