import requests

# Define the bounding box
# Format of the bounding box: “min_latitude, min_longitude, max_latitude, max_longitude”
bbox = "0.0097394039291600,32.4057359175773030,0.5085509362294360,32.7963300045455028"

# Construct the Overpass QL query, find your key value pairs through https://wiki.openstreetmap.org/wiki/Map_features
# This is an xml request: '//' is for commenting out, ';' is for new line
# For Overpass Query Language guideline you can read it through https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide
query = f"""
[out:xml][timeout:25][bbox:{bbox}];
(
    // Built-Up
    //way["building"];
    //relation["building"];
    // Greenspace
    way["natural"];
    relation["natural"];
    // Grayspace (only highways for now, will convert to polygons later)
    //way["highway"~"motorway|primary|secondary|tertiary"];
    // Water Bodies
    //way["natural"="water"];
    //relation["natural"="water"];
    //way["landuse"="basin"];
    //relation["landuse"="basin"];
);
(._;>;);
out body;
"""

# URL to the Overpass API
url = "http://overpass-api.de/api/interpreter"

# Send the request and get the response
response = requests.get(url, params={'data': query})

# Check if the request was successful
if response.status_code == 200:
    # Write response content to an XML file
    with open('osm_data_builtup.xml', 'wb') as file:
        file.write(response.content)
    print("Data has been written to osm_data_builtup.xml")
else:
    print("Error:", response.status_code, response.reason)
