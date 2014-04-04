from django_cron import CronJobBase, Schedule
from django.utils import timezone
from apps.paste.models import Paste

class ClearExpiredPastesJob(CronJobBase):
    """
        Cron job that checks if there are any expired pastes and remove them from database
    """
    
    RUN_EVERY_MINS = 5
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'apps.paste.clear_expired_pastes'
    
    def do(self):
        Paste.objects.filter(expire_date__lte=timezone.now())