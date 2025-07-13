from ultralytics import YOLO
import pandas as pd
from pathlib import Path

# Path to the folder containing images
image_dir = Path("data/raw/telegram_images/2025-07-11")

# Output CSV path
output_csv = Path("data/processed/image_detections.csv")

# Load YOLOv8 model (nano version for speed, can switch to 's' or 'm' for better accuracy)
model = YOLO("yolov8s.pt")
# Set confidence threshold (lower to catch more detections, higher to reduce false positives)
model.conf = 0.2

# List to collect all detections
detections = []

# Iterate over all images in the folder (supporting all image formats)
for image_path in image_dir.glob("*.*"):
    try:
        results = model(image_path)

        for r in results:
            print(f"Image: {image_path.name}, Detections: {len(r.boxes)}")  # Debug line

            for box in r.boxes:
                detection = {
                    "file_name": image_path.name,
                    "message_id": image_path.stem.split("_")[0],  # Extract prefix as message ID
                    "object_class": model.names[int(box.cls)],
                    "confidence_score": float(box.conf)
                }
                detections.append(detection)

    except Exception as e:
        print(f"Error processing {image_path.name}: {e}")

# Convert detections to a DataFrame and save to CSV
df = pd.DataFrame(detections)

# Make sure output folder exists
output_csv.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_csv, index=False)
print(f"\n✅ Saved {len(df)} detections to {output_csv}")


