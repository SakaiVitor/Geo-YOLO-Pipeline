
## README for Geo-YOLO-Pipeline

### Overview
The Geo-YOLO-Pipeline is a Python-based toolkit designed for transforming geospatial data into a format suitable for object detection using the YOLO (You Only Look Once) model. It provides tools to convert TIFF images to PNG, merge shapefiles, and prepare datasets for YOLO detection models. This repository offers a streamlined process for converting geospatial raster data into tiled images, detecting objects within those images, and converting the results back into geospatial formats (shapefiles).

### Key Features
- **TIFF to PNG Conversion:** Convert TIFF images to PNG format for compatibility with many image processing libraries.
- **Shapefile Merging:** Combine multiple shapefiles into a single, comprehensive file.
- **Geotiff Tiling:** Slice large geotiff images into smaller tiles, optimized for object detection.
- **YOLO Detection:** Run object detection on tiled images using a pre-trained YOLO model.
- **Shapefile Generation:** Convert YOLO detection results back into geospatial shapefile format.

### Files and Usage
- `tif_to_png.py`: Script to convert TIFF images to PNG format.
- `merge_shapefiles.py`: Script to merge multiple shapefiles into one.
- `main.py`: The main pipeline script that orchestrates the conversion, detection, and shapefile generation processes.
- `geotiff_tiler.py`: Script to break down geotiff images into smaller, manageable tiles.
- `yolo_to_shp.py`: Convert YOLO model outputs into shapefiles.
- `yolo_detection.py`: Perform object detection using the YOLO model on tiled images.

### Getting Started
1. **Clone the repository:**
   ```
   git clone https://github.com/SakaiVitor/Geo-YOLO-Pipeline.git
   ```
2. **Install Dependencies:**
   Ensure Python 3.x is installed along with the necessary packages:
   ```
   pip install -r requirements.txt
   ```
3. **Running the Pipeline:**
   Execute the `main.py` to start the processing pipeline:
   ```
   python main.py
   ```

### Requirements
- Python 3.x
- Libraries: Listed in `requirements.txt`

