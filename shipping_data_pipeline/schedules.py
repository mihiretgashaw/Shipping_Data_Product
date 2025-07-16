from dagster import ScheduleDefinition
from .jobs import shipping_data_job

shipping_data_schedule = ScheduleDefinition(
    job=shipping_data_job,
    cron_schedule="0 6 * * *",  # every day at 6 AM
)
