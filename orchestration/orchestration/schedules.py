import dagster as dg
from jobs import job_dlt

############################
#         Schedules        #
############################

schedule_dlt = dg.ScheduleDefinition(
    job=job_dlt,
    cron_schedule="0 0 * * *",  # Every day at midnight
    execution_timezone="Europe/Stockholm",
)
