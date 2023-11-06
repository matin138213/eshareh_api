import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

celery = Celery('djangoProject')
celery.config_from_object('django.conf:settings', namespace='CELERY')# config bro as settings bardar
celery.autodiscover_tasks() #find your task celery
