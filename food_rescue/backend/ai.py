from ultralytics import YOLO
from PIL import Image
import numpy as np

# Load once
model = YOLO("yolov8n.pt")

VALID_FOODS = [
    'banana','apple','sandwich','orange','broccoli',
    'carrot','hot dog','pizza','donut','cake'
]

def analyze_image(image: Image.Image):
    results = model(image)
    detected_items = []
    is_food = False

    for result in results:
        for box in result.boxes:
            class_name = model.names[int(box.cls[0])]
            conf = float(box.conf[0])

            if class_name in VALID_FOODS and conf > 0.4:
                detected_items.append(f"{class_name} ({int(conf*100)}%)")
                is_food = True

    return is_food, detected_items
