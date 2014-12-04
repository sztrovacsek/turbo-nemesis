#!/usr/bin/env python
from __future__ import print_function
import boto
from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.key import Key
import time
import os
from PIL import Image

from api.models import Post, FoodPhoto
from api.services import (
    connect_aws, create_thumbnail
)


def create_missing_thumbnails():
    print("Starting: creating missing thumbnails")
    (conn, bucket, bucket_name) = connect_aws();
    posts = Post.objects.all()
    for post in posts:
        foodphoto = post.foodphoto
        if not foodphoto.feed_thumbnail_url:
            print("Post needs thumbnail: {0}".format(
                str(post)))
            create_thumbnail(foodphoto, bucket, bucket_name) 


if __name__ == "__main__":
    create_missing_thumbnails()
