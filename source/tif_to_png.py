import concurrent
import os
import numpy as np
from PIL import Image
import rasterio
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def normalize_and_convert(tif_path, output_dir):
    with rasterio.open(tif_path) as src:
        r = normalize_band(src.read(1))
        g = normalize_band(src.read(2))
        b = normalize_band(src.read(3))
        if r is None or g is None or b is None:
            return  # Skip saving if any band is only nodata
        img_array = np.dstack((r, g, b))
        img = Image.fromarray(img_array)
        png_path = os.path.join(output_dir, os.path.basename(tif_path).replace('.tif', '.png'))
        img.save(png_path)


def tif_to_png(input_dir, output_dir, conversion_type=0):
    os.makedirs(output_dir, exist_ok=True)
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.tif')]
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(normalize_and_convert, tif_path, output_dir) for tif_path in files]
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Converting TIF to PNG"):
            pass


def normalize_band(band):
    band = band.astype(np.float32)
    valid_mask = band != band.min()
    valid_data = band[valid_mask]
    p2, p98 = np.percentile(valid_data, (2, 98))
    band[valid_mask] = np.interp(valid_data, (p2, p98), (0, 255))
    band[~valid_mask] = 0
    return band.astype(np.uint8)

# Example usage
def main():
    input_dir = 'tiled_out'
    output_dir = 'tiled_out_png'
    tif_to_png(input_dir, output_dir)

if __name__ == "__main__":
    main()
