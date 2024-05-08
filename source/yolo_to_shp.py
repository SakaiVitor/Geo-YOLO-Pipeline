import geopandas as gpd
from shapely.geometry import box
import rasterio
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def process_detection(txt_path, tif_path, output_folder):
    base_name = os.path.splitext(os.path.basename(txt_path))[0]
    shp_path = os.path.join(output_folder, base_name + '.shp')

    with rasterio.open(tif_path) as src:
        transform = src.transform
        crs = src.crs

        detections = []
        with open(txt_path, 'r') as file:
            for line in file:
                class_id, x_center, y_center, width, height = map(float, line.split())
                x_min = (x_center - width / 2) * src.width
                y_min = (y_center - height / 2) * src.height
                x_max = (x_center + width / 2) * src.width
                y_max = (y_center + height / 2) * src.height

                min_x, min_y = transform * (x_min, y_min)
                max_x, max_y = transform * (x_max, y_max)

                geom = box(min_x, min_y, max_x, max_y)
                detections.append({'geometry': geom, 'class_id': class_id})

        gdf = gpd.GeoDataFrame(detections, crs=crs)
        gdf.to_file(shp_path, driver='ESRI Shapefile')

def create_shapefile_from_detections(txt_folder, tif_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]
    tasks = [(os.path.join(txt_folder, f), os.path.join(tif_folder, os.path.splitext(f)[0] + '.tif'), output_folder) for f in txt_files]

    with ThreadPoolExecutor(max_workers=8) as executor:
        list(tqdm(executor.map(lambda p: process_detection(*p), tasks), total=len(tasks), desc="Processing shapefiles"))


if __name__ == "__main__":
    txt_folder = 'runs/detect/predict/labels'
    tif_folder = 'tiled_out'
    output_folder = 'detection_shapefiles'
    create_shapefile_from_detections(txt_folder, tif_folder, output_folder)
