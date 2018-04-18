CELERY_IMPORTS = ('run')
CELERY_IGNORE_RESULT = False
BROKER_HOST = '127.0.0.1'
BROKER_PORT = 5672
BROKER_URL = 'amqp://'


from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'mail-every-10-mins':{
        'task': 'run.job',
        'schedule': timedelta(minutes=10),
    }
}
