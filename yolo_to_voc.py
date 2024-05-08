import os
import xml.etree.ElementTree as ET
from PIL import Image


def yolo_to_voc(yolo_file_path, image_folder_path, output_folder_path, class_labels):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Process each YOLO annotation file
    for file in os.listdir(yolo_file_path):
        if file.endswith(".txt"):
            image_path = os.path.join(image_folder_path, file.replace(".txt", ".png"))
            image = Image.open(image_path)
            iw, ih = image.size

            annotation = ET.Element("annotation")
            ET.SubElement(annotation, "folder").text = image_folder_path
            ET.SubElement(annotation, "filename").text = os.path.basename(image_path)

            size = ET.SubElement(annotation, "size")
            ET.SubElement(size, "width").text = str(iw)
            ET.SubElement(size, "height").text = str(ih)
            ET.SubElement(size, "depth").text = "3"  # Assuming the image is RGB

            with open(os.path.join(yolo_file_path, file), 'r') as f:
                for line in f:
                    class_id, x_center, y_center, width, height = map(float, line.split())
                    x_center, width = x_center * iw, width * iw
                    y_center, height = y_center * ih, height * ih
                    x_min = int(round(x_center - (width / 2)))
                    y_min = int(round(y_center - (height / 2)))
                    x_max = int(round(x_center + (width / 2)))
                    y_max = int(round(y_center + (height / 2)))

                    object = ET.SubElement(annotation, "object")
                    ET.SubElement(object, "name").text = class_labels[int(class_id)]
                    ET.SubElement(object, "pose").text = "Unspecified"
                    ET.SubElement(object, "truncated").text = "0"
                    ET.SubElement(object, "difficult").text = "0"
                    bndbox = ET.SubElement(object, "bndbox")
                    ET.SubElement(bndbox, "xmin").text = str(x_min)
                    ET.SubElement(bndbox, "ymin").text = str(y_min)
                    ET.SubElement(bndbox, "xmax").text = str(x_max)
                    ET.SubElement(bndbox, "ymax").text = str(y_max)

            tree = ET.ElementTree(annotation)
            tree.write(os.path.join(output_folder_path, file.replace(".txt", ".xml")))


# Example usage
class_labels = ["0"]  # Example classes
yolo_to_voc("runs/run1/predict/labels", "runs/run1/tiled_png", "runs/run1/voc_annotation", class_labels)
