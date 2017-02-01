from celeryTask import celery


@celery.task
def hello_world(x):
    print(x)