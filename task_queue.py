from celery import Celery

celery = Celery('tasks', backend='redis://localhost', broker='redis://localhost')
