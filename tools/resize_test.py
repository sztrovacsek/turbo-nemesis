#!/usr/bin/env python
from __future__ import print_function
import boto
import time
import os
from PIL import Image

print("Starting")
from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.key import Key

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET')

conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY )
print("Connected to s3")

# print('\n'.join(i for i in dir(Location) if i[0].isupper()))
# bucket = conn.create_bucket('vincang-test', location=Location.EU)
bucket = conn.get_bucket(S3_BUCKET)
print("Looked up bucket {0}".format(S3_BUCKET))

# pocess one image
k = Key(bucket)
k.key = 'dev-1417029035.jpg'
tempfilename = 'norvegia.jpg'
s = k.get_contents_to_filename(tempfilename)
try:
    im = Image.open(tempfilename)
    print(im.format, im.size, im.mode)
    orig_size = im.size
    new_width = 470
    factor = float(new_width)/float(orig_size[0])
    new_height = int(factor*orig_size[1]) 
    print("New sizes: {0}x{1}".format(new_width, new_height))
    im_out = im.resize((new_width, new_height))
    im_out.save('resized_for_feed_{0}'.format(tempfilename), 'JPEG')
except IOError:
    print("IOError", tempfilename)

