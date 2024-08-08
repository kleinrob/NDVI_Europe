#This script connects with OpenEO (account required) and creates a cloud-filtered NDVI composites for a given extent and a number of start and end dates.

import openeo
import pandas as pd
import geopandas as gpd

connection = openeo.connect("openeo.dataspace.copernicus.eu").authenticate_oidc()

dates = pd.read_csv(#CSV_with_start_and_end_dates_for_months)
extent = gpd.read_file(#shp_with_NESW_borders)
output_dir = #output_dir



for index, row in dates.iloc[0:].iterrows():
    date_index = index
      
    bbox=connection.load_collection(
             "SENTINEL2_L2A",
             spatial_extent = {"west": extent.loc[0]["west"], "east": extent.loc[0]["east"], "north": extent.loc[0]["north"], "south": extent.loc[0]["south"]},
             temporal_extent = [dates.loc[date_index]["start"],dates.loc[date_index]["end"]],
             bands=["B04","B08","SCL"],
             max_cloud_cover = 50
             )


    SCL=bbox.band("SCL")
    red= bbox.band("B04")
    nir = bbox.band("B08")
    cloud_mask = (SCL ==8)|(SCL==9)|(SCL==10)
    ndvi_cube = (nir-red)/(nir+red)
    bbox_masked =ndvi_cube.mask(cloud_mask)
    ndvi_composite = bbox_masked.mean_time()
    ndvi_composite.download(f"{output_dir}/{dates.loc[date_index]['start']}.tiff")

	
