import subprocess
import os
from dagster import op
from dotenv import load_dotenv
from scraping.scraper import scrape_channels
import sys

@op
def scrape_telegram_data():
    results = scrape_channels()
    print(f"Scraping results: {results}")

@op
def load_raw_to_postgres():
    load_dotenv()
    env = os.environ.copy()
    subprocess.run(
        [sys.executable, "scripts/load_raw_json_to_pg.py"],
        check=True,
        env=env
    )

@op
def run_dbt_transformations():
    load_dotenv()
    env = os.environ.copy()

    # Replace this path with the absolute path to your dbt project folder
    dbt_project_dir = r"C:\Users\pc\Desktop\10 Academy\Week 7\Shipping_data_product\telegram_project"

    subprocess.run(
        ["dbt", "run"],
        cwd=dbt_project_dir,
        check=True,
        env=env
    )

@op
def run_yolo_enrichment():
    load_dotenv()
    env = os.environ.copy()
    try:
        result = subprocess.run(
            [sys.executable, "scripts/detect_objects.py"],
            check=True,
            env=env,
            capture_output=True,
            text=True,
        )
        print("YOLO STDOUT:", result.stdout)
        print("YOLO STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("YOLO STDOUT:", e.stdout)
        print("YOLO STDERR:", e.stderr)
        raise e
