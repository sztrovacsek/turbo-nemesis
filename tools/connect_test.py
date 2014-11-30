#!/usr/bin/env python
import boto
import time
import os

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

keys= bucket.get_all_keys()
for key in keys:
  print(key)

'''
# download
k = Key(bucket)
k.key = 'dev-1417027608.jpg'
s = k.get_contents_to_filename('bor.jpg')
'''


