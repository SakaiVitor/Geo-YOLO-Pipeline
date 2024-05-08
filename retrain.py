import os
import shutil
import yaml
from ultralytics import YOLO
import random


def copy_files(source_folder, destination_folder, file_extension, file_list=None):
    """Copy specified files or all files from the source to the destination folder."""
    os.makedirs(destination_folder, exist_ok=True)
    files = file_list if file_list is not None else os.listdir(source_folder)
    for file_name in files:
        if file_name.endswith(file_extension):
            shutil.copy2(os.path.join(source_folder, file_name), destination_folder)


def distribute_files(image_folder, label_folder, config):
    # Determine the number of images
    images = [f for f in os.listdir(image_folder) if f.endswith('.png')]
    labels = [f.replace('.png', '.txt') for f in images]

    # Paths from YAML
    train_images_path = os.path.join(config['train'], 'images')
    train_labels_path = os.path.join(config['train'], 'labels')
    val_images_path = os.path.join(config['val'], 'images')
    val_labels_path = os.path.join(config['val'], 'labels')
    test_images_path = os.path.join(config['test'], 'images')
    test_labels_path = os.path.join(config['test'], 'labels')

    # Distribution logic based on the number of images
    if len(images) < 10:
        # Copy all images and labels to the training folders
        copy_files(image_folder, train_images_path, '.png')
        copy_files(label_folder, train_labels_path, '.txt')
    else:
        # Shuffle images for random distribution
        combined = list(zip(images, labels))
        random.shuffle(combined)
        images, labels = zip(*combined)

        # Splitting data
        test_size = val_size = len(images) // 10
        train_size = len(images) - 2 * test_size

        # Copy files to corresponding folders
        copy_files(image_folder, train_images_path, '.png', images[:train_size])
        copy_files(label_folder, train_labels_path, '.txt', labels[:train_size])
        copy_files(image_folder, val_images_path, '.png', images[train_size:train_size + val_size])
        copy_files(label_folder, val_labels_path, '.txt', labels[train_size:train_size + val_size])
        copy_files(image_folder, test_images_path, '.png', images[train_size + val_size:])
        copy_files(label_folder, test_labels_path, '.txt', labels[train_size + val_size:])


def main(image_folder, label_folder, yaml_path, model_weights):
    # Load paths from YAML file
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)

    # Distribute files according to the number of images
    distribute_files(image_folder, label_folder, config)

    # Build model from YAML and load weights
    model = YOLO(model_weights)

    # Train the model
    results = model.train(data=yaml_path, epochs=150, imgsz=320, project="train")
    print("Training completed.")


if __name__ == "__main__":
    image_folder = "/path/to/png_files"
    label_folder = "/path/to/txt_files"
    yaml_path = "Dataset_V5/data.yaml"
    model_weights = 'yolov8x.pt'

    main(image_folder, label_folder, yaml_path, model_weights)
