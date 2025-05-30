import dagster as dg

############################
#         Schedules        #
############################

schedule_dlt = dg.ScheduleDefinition(
    job_name="dlt_job",
    cron_schedule="0 0 * * *",  # Every day at midnight
    execution_timezone="Europe/Stockholm",
)
