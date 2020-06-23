from celery.schedules import crontab
from celery.task import periodic_task
import requests

URL = 'http://62.90.89.14:8000/api/'

@periodic_task(run_every=(crontab(minute=0, hour=4, day_of_week='sun')),
               name="consortium_builder", ignore_result=True)
def consortium_builder():
    """
    automatic task to build consortium and send mail to the user.
    :return:
    """
    url = URL + 'calls/consortium_builder/'
    response = requests.get(url)

# , day_of_month='1-8'
@periodic_task(run_every=(crontab(minute=0, hour=12, day_of_week='fri', day_of_month='1-7')),
               name="update_organizations", ignore_result=True)
def update_organizations():
    """
    automatic task to update organizations from EU.
    :return:
    """
    url = URL + 'organizations/updateOrganizations/'
    response = requests.get(url)

@periodic_task(run_every=(crontab(minute=0, hour=12, day_of_week='fri', day_of_month='1-7')),
               name="update_events", ignore_result=True)
def update_events():
    """
    automatic task to update Events and participants from B2MATCH.
    :return:
    """
    url1 = URL + 'events/update_upcoming_events/'

    response = requests.get(url1)



@periodic_task(run_every=(crontab(minute=0, hour=4, day_of_week='sun')),
               name="update_events", ignore_result=True)
def b2match_alerts():
    url2 = URL + 'alerts/alertB2match/'
    response2 = requests.get(url2)
