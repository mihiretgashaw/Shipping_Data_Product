from ultralytics import YOLO
import os
import pandas as pd
import uuid

# Load YOLO model
model = YOLO("yolov8n.pt")  # or yolov8s.pt

# Image directory (from Task 1)
image_folder = "data/raw/telegram_messages/2025-07-11"

output = []

# Scan all images in the folder
for file in os.listdir(image_folder):
    if file.lower().endswith((".jpg", ".png", ".jpeg")):
        image_path = os.path.join(image_folder, file)
        results = model(image_path)[0]

        for box in results.boxes:
            output.append({
                "detection_id": str(uuid.uuid4()),
                "file_name": file,
                "object_class": model.names[int(box.cls)],
                "confidence_score": float(box.conf)
            })

# Save detections
df = pd.DataFrame(output)
df.to_csv("data/yolo_detections.csv", index=False)
