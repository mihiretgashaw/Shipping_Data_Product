Shipping Data Product – Telegram Medical Marketplace Analytics

This project transforms messy Telegram e-commerce data into structured, trusted insights using a modern data stack.

Task 1 - Scraping and Loading Telegram Messages

Extract messages from public Telegram channels using the Telegram API.

Save messages in JSON format.

Load the JSON into the raw.telegram_messages table in PostgreSQL.

Task 2 - Data Modeling and Transformation with DBT

Create staging models to clean and normalize raw data.

Build data mart models using star schema:

dim_channels, dim_dates, fct_messages

Validate with tests (unique, not_null, and one custom test).

Use dbt docs to generate documentation.

Task 3 – YOLOv8 Image Detection Enrichment
Integrate YOLOv8 to detect objects (e.g., medical products) in images shared on Telegram.

Run inference on downloaded media using ultralytics/yolov8.

Save detection results (object class, confidence score) to data/yolo_detections.csv.

Load detections into the raw.image_detections table in PostgreSQL for further analysis.

Task 4 – Build an Analytical API (FastAPI)
Develop an Analytical API using FastAPI to expose insights from the analytics layer.

Key endpoints:

/top-products: Returns top-mentioned or detected products.

/channel-activity: Tracks message frequency per channel.

API pulls structured data directly from the PostgreSQL analytics tables.

Task 5 – Pipeline Orchestration (Dagster)
Orchestrate the full pipeline using Dagster:

scrape_telegram_data: Scrapes and stores raw messages.

load_raw_to_postgres: Loads JSON into the raw layer.

run_dbt_transformations: Triggers dbt to build analytics models.

run_yolo_enrichment: Executes YOLO detection and loads results.

Define dependencies and execution flow through Dagster @op and @job.

Enable modular, observable, and maintainable workflow execution.
