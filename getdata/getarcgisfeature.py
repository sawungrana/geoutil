import requests
import geopandas as gpd

# ArcGIS FeatureServer endpoint
url = "https://services1.arcgis.com/3YlK2vfHGZtonb1r/arcgis/rest/services/Zonnepanelen_Zwolle/FeatureServer/0/query"

# Query params to fetch data in GeoJSON
params = {
    'where': '1=1',  # This condition effectively selects all features
    'outFields': '*',  # Select all fields
    'outSR': '4326',  # Request data in WGS 84 coordinate reference system
    'f': 'geojson'  # Request output format as GeoJSON
}

# Send request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse GeoJSON
    
    # Convert GeoJSON to GDF
    gdf = gpd.GeoDataFrame.from_features(data)
    
    # Output path for gpkg
    output_path = "zonnepanelen_zwolle.gpkg" # Adjust the name as you want
    
    # Export GDF to gpkg
    gdf.to_file(output_path, driver="GPKG")
    
    print(f"Data exported to: {output_path}")
else:
    print("Failed to fetch data:", response.status_code)
