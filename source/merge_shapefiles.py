import geopandas as gpd
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd
from tqdm import tqdm


def merge_individual_shapefile(shp_path):
    return gpd.read_file(shp_path)


def merge_shapefiles(input_folder, output_file):
    shapefiles = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.shp')]

    with ProcessPoolExecutor(max_workers=8) as executor:
        # Submit jobs to executor
        future_to_shp = {executor.submit(merge_individual_shapefile, shp): shp for shp in shapefiles}
        results = []

        # Set up the progress bar to cover reading and merging
        with tqdm(total=len(shapefiles) + 1, desc="Processing and Merging Shapefiles") as pbar:
            for future in as_completed(future_to_shp):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Failed to process {future_to_shp[future]}: {e}")
                pbar.update(1)

            # Merge all GeoDataFrames into a single GeoDataFrame outside the loop but within the progress bar context
            if results:
                merged_gdf = gpd.GeoDataFrame(pd.concat(results, ignore_index=True))
                merged_gdf.to_file(output_file, driver='ESRI Shapefile')
                print(f"Merged shapefile saved as: {output_file}")
                pbar.update(1)


# Incorporating module call into the main function
def main():
    shp_output_folder = "runs/run1/detection_shapefiles"
    merged_shp_output_file = os.path.join(shp_output_folder, "merged_shapefile.shp")

    merge_shapefiles(shp_output_folder, merged_shp_output_file)


if __name__ == "__main__":
    main()
