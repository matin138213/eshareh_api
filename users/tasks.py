from celery import shared_task
from decouple import config

from djangoProject.melipayamak.sms import Rest


@shared_task
def send_sms(to, token):
    username = config('SMS_USERNAME')
    password = config('SMS_PASSWORD')
    api = Rest(username, password)
    _from = config('SMS_HOST')
    text = str(token)
    response = api.send_by_base_number(to=to, text=text, bodyId=144887)
    print(response)
    return response
