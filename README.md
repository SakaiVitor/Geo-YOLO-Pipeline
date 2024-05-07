
# Geo-YOLO-Pipeline

## Description
The Geo-YOLO-Pipeline is a geospatial processing pipeline developed to facilitate object detection in geospatial images using the YOLO (You Only Look Once) model. This pipeline automates the conversion of GeoTIFF images into formats suitable for training and inference with YOLO, and subsequently converts model outputs into shapefiles for use in Geographic Information Systems (GIS).

## Features
- **GeoTIFF Image Tiling**: Splits large GeoTIFF images into smaller, manageable tiles.
- **Conversion to PNG**: Converts GeoTIFF tiles into PNG images suitable for YOLO processing.
- **Object Detection with YOLO**: Uses YOLO models to detect objects in PNG images.
- **Shapefile Generation**: Converts YOLO detection outputs back into geospatial formats (shapefiles) for GIS analysis.

## Prerequisites
Before you begin, ensure you have Python 3.8+ installed on your machine. Additionally, the following Python libraries are required and can be installed via pip:

```bash
pip install -r requirements.txt
```

## Installation
Clone the repository using:
```bash
git clone https://github.com/SakaiVitor/Geo-YOLO-Pipeline.git
cd Geo-YOLO-Pipeline
```

## Usage
To use the pipeline, follow these steps:

1. **Prepare Your Data**: Place your GeoTIFF images in the appropriate directory.
2. **Run the Pipeline**:
   ```bash
   python main.py
   ```
   Modify `main.py` as needed to point to your specific files and output directories.

## Step-by-Step Operation
1. **Dividing GeoTIFF Images**: Large GeoTIFF images are split into smaller tiles, typically 320x320 pixels, to fit the input size requirements of YOLO and to make processing manageable.
2. **Converting to PNG**: The tiles are converted from GeoTIFF to PNG format, which is necessary for YOLO processing.
3. **Object Detection Using YOLO**: The YOLO model performs object detection on these PNG images. The results are saved as text files containing bounding box coordinates and object classifications.
4. **Converting Detections into Shapefiles**: The bounding box coordinates are converted back into the geospatial coordinates of the original GeoTIFF files. This allows the detection results to be visualized and analyzed in GIS software.
5. **Concatenating Shapefiles**: After processing multiple tiles, each resulting in an individual shapefile, this step merges all these shapefiles into a single file. This facilitates the overall visualization and analysis of detection results on one GIS layer.

## Authors
- **Vitor Sakai** - *Initial work* - [SakaiVitor](https://github.com/SakaiVitor)
