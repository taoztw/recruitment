
# 启动celery
celery --app recruitment worker -l info -P eventlet


# 启动flower
celery -A recruitment flower


# 定时任务
celery -A recruitment beat --scheduler django_celery_beat.schedulers:DatabaseScheduler