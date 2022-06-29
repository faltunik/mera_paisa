from __future__ import absolute_import
import os
from celery import Celery
import dotenv


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'txn.settings')

app = Celery('txn'
            )

app.config_from_object('django.conf:settings', namespace='CELERY')
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
dotenv.load_dotenv(env_file)

app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    pass