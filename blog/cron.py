#requirements for cron class
from django_cron import CronJobBase, Schedule


# Cron Classes starts here

class MyCronJob(CronJobBase):
    RUN_AT_TIMES = ['08:30']

    schedule = Schedule(run_at_times = RUN_AT_TIMES)
    code = 'blog.my_cron_job' # a unique code

    def do(self):
        pass