from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def test_send(message):
    print(message)


@shared_task
def add(a, b):
    print("定时任务")
    return a + b
