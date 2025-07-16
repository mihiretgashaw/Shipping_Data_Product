from dagster import repository
from .jobs import shipping_data_job  # adjust import if needed

@repository
def my_repo():
    return [shipping_data_job]
