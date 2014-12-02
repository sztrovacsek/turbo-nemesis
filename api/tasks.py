from __future__ import absolute_import
import time

from celery import shared_task

from .models import Post, FoodPhoto


@shared_task
def async_task_phase1(task_id, x):
    print('Handling async task phase 1')
    time.sleep(3)
    async_task_phase2.delay(task_id, x)
    print('Firing async task phase 2')
    return True


@shared_task
def async_task_phase2(task_id, x):
    print('Handling async task phase 2')
    time.sleep(7)
    print('Cube saving done')
    return True

