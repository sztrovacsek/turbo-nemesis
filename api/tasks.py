import logging
import time

from celery import shared_task

from .models import Post, FoodPhoto
import services


logger = logging.getLogger(__name__)


@shared_task
def worker_create_thumbnail(post_id):
    logger('Worker: create thumbnail for {0}'.format(post))
    post = Post.objects.filter(post_id).first()
    if post:
        services.create_missing_thumbnail(post)
    logger('Worker: done')

