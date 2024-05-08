import os
from source.geotiff_tiler import divide_geotiff
from source.tif_to_png import tif_to_png
from source.yolo_detection import run_yolo_detection
from source.yolo_to_shp import create_shapefile_from_detections
from source.merge_shapefiles import merge_shapefiles


def get_next_run_folder(base_path):
    # Cria a pasta runs se não existir
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        return os.path.join(base_path, 'run1')

    # Encontrar o próximo número de run
    previous_runs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d)) and d.startswith('run')]
    if not previous_runs:
        return os.path.join(base_path, 'run1')
    max_run = max(int(run.split('run')[1]) for run in previous_runs)
    next_run = max_run + 1
    return os.path.join(base_path, f'run{next_run}')

def main():
    base_path = 'runs'
    run_folder = get_next_run_folder(base_path)

    # Estrutura de pastas dentro da run
    output_folder = os.path.join(run_folder, 'tiled_tif')
    png_output_folder = os.path.join(run_folder, 'tiled_png')
    labels_output_folder = os.path.join(run_folder, '')
    shp_output_folder = os.path.join(run_folder, 'detection_shapefiles')
    merged_shp_output_file = os.path.join(shp_output_folder, "merged_shapefile.shp")

    # Assegura a criação das pastas necessárias
    for folder in [output_folder, png_output_folder, labels_output_folder, shp_output_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    input_file = "clip_geo_Mosaic_PNEO_T01_v02 2.tif"

    # Dividir GEOTIF em tiles
    divide_geotiff(input_file, output_folder)

    # Converter TIF para PNG
    tif_to_png(output_folder, png_output_folder, conversion_type=0)  # Altere para 1 para NDVI, etc.

    # Realizar a detecção usando YOLO
    run_yolo_detection(png_output_folder, labels_output_folder)

    # Converter detecções do YOLO em arquivos SHP
    create_shapefile_from_detections(os.path.join(run_folder, 'predict/labels'), output_folder, shp_output_folder)

    # Mesclar os shapefiles
    merge_shapefiles(shp_output_folder, merged_shp_output_file)


if __name__ == "__main__":
    main()
