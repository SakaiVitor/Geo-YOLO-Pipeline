import os
from ultralytics import YOLO


def run_yolo_detection(input_dir, output_dir, model_path='best.pt'):
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    # Load the pretrained YOLO model
    model = YOLO(model_path)

    # Run inference on 'bus.jpg' with arguments
    model.predict(input_dir, save=True, imgsz=320, conf=0.25, iou=0.2,
                  augment=True, max_det=500,
                  save_txt=True, show_labels=False, show_conf=False, line_width=2)


def main():
    input_dir = 'tiled_out_png'  # Directory containing PNG images
    output_dir = 'tiled_out_png_labels'  # Directory to save YOLO format labels and annotated images
    run_yolo_detection(input_dir, output_dir)


if __name__ == "__main__":
    main()
