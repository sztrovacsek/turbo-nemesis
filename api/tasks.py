import logging
import time

from celery import shared_task

from .models import Post, FoodPhoto
from .services import create_missing_thumbnail


logger = logging.getLogger(__name__)


@shared_task
def worker_create_thumbnail(post_id):
    logger.debug('Worker: create thumbnail for {0}'.format(post_id))
    post = Post.objects.filter(pk=post_id).first()
    if post:
        create_missing_thumbnail(post)
    logger.debug('Worker: done')

