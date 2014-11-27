import logging
import json
import time

import time, os, base64, hmac, urllib
from hashlib import sha1

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import *


logger = logging.getLogger(__name__)


def api_backend_login(request):
    if not request.is_ajax():
        return HttpResponse()

    if request.user.is_authenticated():
        return HttpResponse()

    data = request.POST
    print("Post data: {0}".format(data));
    fbUid = data["fbUid"]
    if fbUid:
        user = User.objects.filter(username=fbUid)
        if user:
            print("Already logged in, wtf? ({0})".format(fbUid));
        elif user is not None:
            print("Create and log in user ({0})".format(fbUid));
            user = User.objects.create_user(
                username=fbUid,
                password='dummy')
            user.save()
        # TODO: use our own auth backend
        user = authenticate(username=fbUid, password='dummy')
        if user is not None:
            login(request, user)
            '''
            # TODO: fix this
            fbData = data["fbData"]
            fb_user = FacebookUser.objects.create(
                user_id=user.pk,
                fb_name = fbData["name"],
                fb_first_name = fbData["first_name"],
                fb_last_name = fbData["last_name"],
                fb_email = fbData["email"],
            )
            fb_user.save()
            user.email = fb_user.email
            user.save()
            '''
        
    reply = {"reply": "OK", "user": user.username}
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def api_test(request):
    reply = {"reply": "OK",}
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def api_user_data(request):
    reply = {
        "reply_to": "api_user_data",
        "username": request.user.username,
        "first_name": request.user.first_name,
    }
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def api_sign_s3(request):
    print("Signing aws request")
    # Load necessary information into the application:
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')

    # Collect information on the file from the GET parameters of the request:
    mime_type = request.GET['s3_object_type']
    
    # Come up with a filename
    object_name = '{0}-{1}.jpg'.format(request.user, int(time.time()))

    # Set the expiry time of the signature (in seconds) and declare the permissions of the file to be uploaded
    expires = int(time.time()+10)
    amz_headers = "x-amz-acl:public-read"
 
    # Generate the PUT request that JavaScript will use:
    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)
     
    # Generate the signature with which the request can be signed:
    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY.encode(), put_request.encode(), sha1).digest())
    # Remove surrounding whitespace and quote special characters:
    signature = urllib.parse.quote_plus(signature.strip())

    # Build the URL of the file in anticipation of its imminent upload:
    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
        'url': url
    })
    print("Aws PUT request signed: {0}".format(content))
    
    # Return the signed request and the anticipated URL back to the browser in JSON format:
    return HttpResponse(
        content,
        content_type='application/json'
    )


@login_required
def api_photo_add(request):
    if not request.is_ajax():
        return HttpResponse()

    print("Request (add photo) received: {0}".format(request.POST));
    photo_url = request.POST.get('photo_url', '')
    photo = FoodPhoto(photo_url=photo_url)
    photo.save()
    print("Photo saved: {0}".format(photo.photo_url));
    description = request.POST.get('description', '')
    post = Post(user=request.user, foodphoto=photo, description=description)
    post.save()
    print("Post saved: {0}".format(post.description));

    reply = {
        "reply_to": "api_photo_add",
        "username": request.user.username,
        "reply": "OK",
    }
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


def api_latest_posts(request):
    reply = {
        "reply_to": "api_latest_posts",
        "username": request.user.username,
    }
    qs = Post.objects.all().order_by('create_time')
    reply["posts"] = [{
        "create_date": str(post.create_time),
        "description": post.description,
        "photo_url": post.foodphoto.photo_url,
        } for post in qs.reverse()[:5]]
    reply["reply"] = "OK"
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )



