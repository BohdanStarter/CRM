import logging
from huey.contrib.djhuey import periodic_task
from django.utils import timezone
from huey import crontab
from licenses.models import License

logger = logging.getLogger(__name__)

@periodic_task(crontab.hourly())
def status_update_task():
    logger.info("Starting expiration check...")
    try:
        license_counter = 0
        for license in License.objects.filter(status__exact=License.ACTIVE).filter(expiration_date__lte=timezone.now()):
            license.update_status()
            license_counter += 1
        if license_counter == 0:
            logger.info("No license to update for now.")
        else:
            logger.info(f"{license_counter} - licenses have been updated successfully!")
    except Exception as e:
        logger.error(f"Task failed! Error details: {str(e)}")
