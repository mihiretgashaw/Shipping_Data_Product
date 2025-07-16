# from ultralytics import YOLO
# import os
# import pandas as pd

# # Initialize the model
# model = YOLO('yolov8s.pt')  

# # Path to raw image folder
# image_folder = "data/raw/telegram_messages/2025-07-11"

# # Output list
# detections = []

# # Loop through image files
# for filename in os.listdir(image_folder):
#     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#         image_path = os.path.join(image_folder, filename)
#         results = model(image_path)[0]
        
#         for box in results.boxes:
#             detections.append({
#                 "image_name": filename,
#                 "detected_object_class": model.names[int(box.cls)],
#                 "confidence_score": float(box.conf)
#             })

# # Convert to DataFrame
# df = pd.DataFrame(detections)

# # Save results
# os.makedirs("data/processed", exist_ok=True)
# df.to_csv("data/processed/image_detections.csv", index=False)

# print(f"[INFO] Saved {len(df)} detections to data/processed/image_detections.csv")

from ultralytics import YOLO
import cv2
import os
import pandas as pd
import psycopg2

# === CONFIG ===
IMAGE_DIR = "data/raw/telegram_messages/2025-07-11" # path where Task 1 saved the scraped images
DB_CONFIG = {
    'host': 'localhost',
    'port': '5433',
    'dbname': 'telegram_db',
    'user': 'postgres',
    'password': 'admin'
      
}
MODEL_PATH = "yolov8s.pt"

# === LOAD MODEL ===
model = YOLO(MODEL_PATH)

# === CONNECT TO DB ===
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# === RUN DETECTION ===
def detect_objects(image_path):
    results = model(image_path)
    data = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls = result.names[int(box.cls)]
            score = float(box.conf)
            data.append({
                "file_name": os.path.basename(image_path),
                "object_class": cls,
                "confidence_score": round(score, 4)
            })
    return data

# === MAIN ===
def main():
    all_detections = []

    for file in os.listdir(IMAGE_DIR):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            full_path = os.path.join(IMAGE_DIR, file)
            detections = detect_objects(full_path)
            all_detections.extend(detections)

    df = pd.DataFrame(all_detections)
    if df.empty:
        print("No detections.")
        return

    # === OPTIONAL: Store to Postgres (staging) ===
    with connect_db() as conn:
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO stg_image_detections (file_name, object_class, confidence_score)
                VALUES (%s, %s, %s)
                """,
                (row["file_name"], row["object_class"], row["confidence_score"])
            )
        conn.commit()

if __name__ == "__main__":
    main()
