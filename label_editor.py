import os
import subprocess


def open_label_editor():
    labels_folder = "runs/run1/predict/labels"
    images_folder = "runs/run1/predict"
    labelimg_path = "labelImg"

    # Iniciar labelImg com os diretórios apropriados
    subprocess.run([labelimg_path, images_folder, labels_folder])

