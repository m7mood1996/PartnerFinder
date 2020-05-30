from celery.schedules import crontab
from celery.task import periodic_task
import requests


@periodic_task(run_every=(crontab(minute=0, hour=6)),
               name="consortium_builder", ignore_result=True)
def consortium_builder():
    """
    automatic task to build consortium and send mail to the user.
    :return:
    """
    url = 'http://127.0.0.1:8000/api/calls/consortium_builder/'
    response = requests.get(url)

# , day_of_month='1-8'
@periodic_task(run_every=(crontab(minute=0, hour=15, day_of_week='fri')),
               name="update_organizations", ignore_result=True)
def update_organizations():
    """
    automatic task to update organizations from EU.
    :return:
    """
    url = 'http://127.0.0.1:8000/api/organizations/updateOrganizations/'
    response = requests.get(url)
