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


AWS_PREFIX = 'https://s3-eu-west-1.amazonaws.com/'
TMP_ORIG = 'orig_tmp.jpg'
TMP_NEW = 'thumbnail_feed_tmp.jpg'


def aws_bucket_prefix(bucket_name):
    s = AWS_PREFIX + bucket_name + '/' 
    return s


def url_prefix_magic(bucket_name):
    l = len(AWS_PREFIX) + len(bucket_name) + 1
    return l

    
def connect_aws():
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')

    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY )
    print("Connected to s3")

    bucket = conn.get_bucket(S3_BUCKET)
    print("Looked up bucket {0}".format(S3_BUCKET))
    return (conn, bucket, S3_BUCKET)


def create_thumbnail(foodphoto, bucket, prefix_lengh, bucket_name):
    # download orig
    k = Key(bucket)
    print("FoodPhoto url: {0}".format(foodphoto.photo_url))
    trunkname = foodphoto.photo_url[prefix_lengh:] 
    print("Trunk name: {0}".format(trunkname))
    k.key = trunkname
    s = k.get_contents_to_filename(TMP_ORIG)
    # create thumbnail
    try:
        im = Image.open(TMP_ORIG)
        print(im.format, im.size, im.mode)
        orig_size = im.size
        new_width = 470
        factor = float(new_width)/float(orig_size[0])
        new_height = int(factor*orig_size[1]) 
        print("New sizes: {0}x{1}".format(new_width, new_height))
        im_out = im.resize((new_width, new_height))
        im_out.save(TMP_NEW, 'JPEG')
    except IOError:
        print("IOError", TMP_ORIG)
    # upload
    k2 = Key(bucket)
    thumb_trunkname = 't_feed_{0}'.format(trunkname)
    print("ThumbTrunk name: {0}".format(thumb_trunkname))
    k2.key = thumb_trunkname 
    k2.set_contents_from_filename(TMP_NEW)
    # save
    url = aws_bucket_prefix(bucket_name)+thumb_trunkname
    print("ThumbUrl name: {0}".format(url))
    foodphoto.feed_thumbnail_url = url
    foodphoto.save()
    # delete temp files
    os.remove(TMP_ORIG)
    os.remove(TMP_NEW)
     

def create_missing_thumbnails():
    print("Starting: creating missing thumbnails")
    (conn, bucket, bucket_name) = connect_aws();
    posts = Post.objects.all()
    # warning: this magic only works if all files are in the same bucket
    prefix_length = url_prefix_magic(bucket_name)
    for post in posts:
        foodphoto = post.foodphoto
        if not foodphoto.feed_thumbnail_url:
            print("Post needs thumbnail: {0}".format(
                str(post)))
            create_thumbnail(foodphoto, bucket, prefix_length, bucket_name) 


if __name__ == "__main__":
    create_missing_thumbnails()
