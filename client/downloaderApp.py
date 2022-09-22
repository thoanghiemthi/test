
from celery import Celery
appcelery = Celery('savedata', backend='rpc://', broker='amqp://guest@localhost//')
appcelery.conf.timezone = 'UTC'


@appcelery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)
@appcelery.task
def test(arg):
    for i in range(1000):

        print(str(i) + arg)