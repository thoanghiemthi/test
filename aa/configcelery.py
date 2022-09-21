from celery.schedules import crontab
CELERY_IMPORTS = ('celeryapp.task.save_issue')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZON = "UTC"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER ='json'
CELERY_RESULT_SERIALZER = 'json'
CELERYBEAT_SCHAEDULE = {'test-celery': {
        'task': 'app.tasks.test.print_hello',
        # Every minute
        'schedule': crontab(minute="*"),
    }}