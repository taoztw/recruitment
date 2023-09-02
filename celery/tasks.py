from celery import Celery

app = Celery('hello', backend='redis://127.0.0.1:6379/0',broker='redis://127.0.0.1:6379/1')

@app.task
def hello(x,y):
    return x+y