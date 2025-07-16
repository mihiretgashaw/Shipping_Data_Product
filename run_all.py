import subprocess

print("🧪 Running Dagster jobs...")
# subprocess.run(["dagster", "job", "launch", "..."])

print("🧹 Running dbt transformations...")
subprocess.run(["dbt", "run"], cwd="dbt")

print("📦 Starting FastAPI app...")
subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])

