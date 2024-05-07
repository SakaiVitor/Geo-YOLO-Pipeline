import os
import sys
from geotiff_tiler import divide_geotiff
from tif_to_png import tif_to_png
from yolo_detection import run_yolo_detection  # Assegure-se de que este módulo está importado corretamente
from yolo_to_shp import create_shapefile_from_detections  # Importa o módulo de conversão para SHP
from merge_shapefiles import merge_shapefiles
def main():
    input_file = "clip_geo_Mosaic_PNEO_T01_v02 2.tif"
    output_folder = "tiled_out"
    png_output_folder = output_folder + "_png"
    labels_output_folder = png_output_folder + "_labels"  # Pasta para salvar os rótulos do YOLO
    shp_output_folder = "detection_shapefiles"  # Pasta para salvar os shapefiles
    merged_shp_output_file = os.path.join(shp_output_folder, "merged_shapefile.shp")

    # Dividir GEOTIF em tiles
    divide_geotiff(input_file, output_folder)

    # Converter TIF para PNG
    tif_to_png(output_folder, png_output_folder, conversion_type=0)  # Altere para 1 para NDVI, etc.

    # Realizar a detecção usando YOLO
    run_yolo_detection(png_output_folder, labels_output_folder)

    # Converter detecções do YOLO em arquivos SHP usando os TIFs tiled
    create_shapefile_from_detections("runs/detect/predict/labels", output_folder, shp_output_folder)

    merge_shapefiles(shp_output_folder, merged_shp_output_file)


if __name__ == "__main__":
    main()
