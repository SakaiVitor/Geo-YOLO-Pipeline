import os
import rasterio
from rasterio.windows import Window
from tqdm import tqdm
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed


def process_tile(input_file, output_dir, i, j, width, height, tile_size, nodata_value):
    window = Window(j, i, min(tile_size, width - j), min(tile_size, height - i))
    with rasterio.open(input_file) as src:
        data = src.read(window=window)
        if np.all(data == nodata_value):
            return f"Tile at {i}, {j} is completely null."
        output_path = os.path.join(output_dir, f'tile_{i}_{j}.tif')
        with rasterio.open(
            output_path, 'w',
            driver='GTiff',
            height=window.height,
            width=window.width,
            count=src.count,
            dtype=src.dtypes[0],
            crs=src.crs,
            transform=rasterio.windows.transform(window, src.transform),
            nodata=nodata_value
        ) as dst:
            dst.write(data)
    return None

def divide_geotiff(input_file, output_dir, tile_size=320):
    os.makedirs(output_dir, exist_ok=True)
    null_tiles_path = os.path.join(output_dir, "null_tiles.txt")

    with rasterio.open(input_file) as src:
        width, height = src.width, src.height
        total_tiles = ((height + tile_size - 1) // tile_size) * ((width + tile_size - 1) // tile_size)
        nodata_value = src.nodata

        # Using ProcessPoolExecutor to parallelize tile processing
        with ProcessPoolExecutor(max_workers=8) as executor:
            futures = {}
            for i in range(0, height, tile_size):
                for j in range(0, width, tile_size):
                    future = executor.submit(process_tile, input_file, output_dir, i, j, width, height, tile_size, nodata_value)
                    futures[future] = (i, j)

            # Progress bar setup
            pbar = tqdm(total=total_tiles, desc="Processing Tiles")
            for future in as_completed(futures):
                result = future.result()
                if result:
                    with open(null_tiles_path, 'a') as null_tiles:
                        null_tiles.write(result + "\n")
                pbar.update(1)
            pbar.close()



if __name__ == "__main__":
    input_file = "clip_geo_Mosaic_PNEO_T01_v02 2.tif"
    output_folder = "tiled_out"
    tile_size = 320
    divide_geotiff(input_file, output_folder, tile_size)
