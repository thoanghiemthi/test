from celery import Celery

app = Celery('dddddd', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y