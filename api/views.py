import logging
import json
import time
import facepy
import os
import urllib
import random

import base64, hmac
from hashlib import sha1

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import *
from .tasks import *


logger = logging.getLogger(__name__)


DEFAULT_MAP_THUMB = 'https://s3-eu-west-1.amazonaws.com/prandius/t_map_post_placeholder.png'


@ensure_csrf_cookie
def api_csrf_token(request):
    # send csrf token
    data = {"reply": "OK"}
    return HttpResponse(
        json.dumps(data, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


def api_backend_login(request):
    if not request.is_ajax():
        return HttpResponse()

    # only take this shortcut for admin users
    if request.user.is_authenticated() and request.user.is_superuser:
        logger.debug(
            "Superuser already logged in: {0}".format(request.user.username))
        return HttpResponse()

    data = request.POST
    logger.debug("Post data: {0}".format(data));
    fbUid = data['fbUid']
    fbName = data['name']
    fbAccessToken = data['accessToken']
    logger.debug("Logging in with facebook: {0} - {1}".format(fbName, fbUid))

    fb_app_id = os.environ.get('FB_APP_ID', '')
    fb_app_secret_key = os.environ.get('FB_APP_SECRET_KEY', '')
    # get the accessToken, and verify with the app secret
    # convert it into a long term token (use app id and app secret)
    try:
        fbLongAccessToken, expires_at = facepy.get_extended_access_token(
            fbAccessToken, fb_app_id, fb_app_secret_key)
        logger.debug(
            "facebook access token valid: {0}, long token: {1}"
            "".format(fbAccessToken, fbLongAccessToken))
    except facepy.exceptions.OAuthError:
        logger.debug("facebook access token failed: {0}".format(fbAccessToken))
        reply = {"reply": "ERROR", "user": user.username}
        return HttpResponse(
            json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
            content_type='application/json'
        )
    if fbUid:
        user = User.objects.filter(username=fbUid)
        if user:
            logger.debug("Logging in existing user: {0} - {1}".format(fbName, fbUid))
        elif user is not None:
            logger.debug("Logging in new user: {0} - {1}".format(fbName, fbUid))
            user = User.objects.create_user(
                username=fbUid,
                first_name = fbName,
                password='dummy')
            user.save()
        # we don't use password based authentication (dummy pw)
        user = authenticate(username=fbUid, password='dummy')
        if user is not None:
            login(request, user)
            fb_user = FacebookUser(
                user_id=user,
                fb_name = data.get('fbData[name]', 'fb_name'),
                fb_first_name = data.get('fbData[first_name]', 'fb_first_name'),
                fb_last_name = data.get('fbData[last_name]', 'fb_last_name'),
                fb_email = data.get('fbData[email]', 'fb_email'),
            )
            fb_user.save()
            user.email = fb_user.fb_email
            user.save()
        
    reply = {"reply": "OK", "user": user.username}
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


def api_backend_logout(request):
    if not request.is_ajax():
        return HttpResponse()

    # only take this shortcut for admin users
    if request.user.is_authenticated():
        logger.debug("Logging out: {0}".format(request.user.username))
        logout(request)

    reply = {"reply": "OK", "user": request.user.username}
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def api_test(request):
    logger.debug("api_test called")
    reply = {"reply": "OK",}
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def api_sign_s3(request):
    logger.debug("Signing aws request")
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
    logger.debug("Aws PUT request signed: {0}".format(content))
    
    # Return the signed request and the anticipated URL back to the browser in JSON format:
    return HttpResponse(
        content,
        content_type='application/json'
    )


@login_required
def api_photo_add(request):
    if not request.is_ajax():
        return HttpResponse()

    logger.debug("Request (add photo) received: {0}".format(request.POST));
    photo_url = request.POST.get('photo_url', '')
    photo = FoodPhoto(photo_url=photo_url)
    photo.save()
    logger.debug("Photo saved: {0}".format(photo.photo_url));
    description = request.POST.get('description', '')
    post = Post(user=request.user, foodphoto=photo, description=description)
    post.save()
    # create thumbnail
    worker_create_thumbnail.delay(post.pk)
    worker_create_map_thumbnail.delay(post.pk)
    logger.debug("Post saved: {0}".format(post.description));

    reply = {
        "reply_to": "api_photo_add",
        "username": request.user.username,
        "reply": "OK",
    }
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def api_post_delete(request):
    if not request.is_ajax():
        return HttpResponse()

    logger.debug("Request (delete post) received: {0}".format(request.POST))
    post_id = request.POST.get('post_id', '')
    post = Post.objects.filter(pk=post_id).first()
    reply = {
        "reply_to": "api_post_delete",
        "username": request.user.username,
    }
    if post and post.user == request.user:
        post.delete()
        logger.debug("Post deleted: {0}".format(post.description))
        reply["reply"] = "OK"
    else:
        logger.debug("Error in post delete: {0}".format(post.description))
        reply["reply"] = "ERROR"

    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def api_post_edit(request):
    if not request.is_ajax():
        return HttpResponse()

    logger.debug("Request (edit post) received: {0}".format(request.POST));
    post_id = request.POST.get('post_id', '')
    description = request.POST.get('description', '')
    address_raw = request.POST.get('address_raw', '')
    coords_x = request.POST.get('coords_x', '')
    coords_y = request.POST.get('coords_y', '')
    post = Post.objects.filter(pk=post_id).first()
    reply = {
        "reply_to": "api_post_edit",
        "username": request.user.username,
    }
    if post and post.user == request.user:
        post.description = description
        post.address_raw = address_raw
        post.coords_x = float(coords_x)
        post.coords_y = float(coords_y)
        # TODO: update location
        post.save()
        logger.debug("Post edited: {0}".format(post.description))
        reply["reply"] = "OK"
    else:
        logger.debug("Error in post edit: {0}".format(post.description))
        reply["reply"] = "ERROR"

    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


def post_data(post):
    data = {
        "create_date": str(post.create_time),
        "description": post.description,
        "photo_url": post.foodphoto.get_photo_url(),
        "photo_url_large": post.foodphoto.photo_url,
        "photo_url_map": DEFAULT_MAP_THUMB,
        "user_name": post.user.first_name,
        "post_id": post.pk,
        "permalink": "/index.html#/post/{0}".format(post.pk),
        "permalink_fb": "/api/post_detail_fb/{0}".format(post.pk),
        "coords": {
            "latitude": 52.08+random.random()-0.5,
            "longitude": 5.10+random.random()-0.5,
        },
        "address_raw": "Paris",
    }
    if post.address_raw:
        data["address_raw"] = post.address_raw
        data["coords"] = {
            "latitude": post.coords_x,
            "longitude": post.coords_y,
        }
    if post.foodphoto.map_thumbnail_url:
        data["photo_url_map"] = post.foodphoto.map_thumbnail_url
    return data

def api_latest_posts(request):
    reply = {
        "reply_to": "api_latest_posts",
        "username": request.user.username,
    }
    qs = Post.objects.all().order_by('create_time')
    reply["posts"] = [post_data(post) for post in qs.reverse()[:10]]
    reply["reply"] = "OK"
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


def api_user_login_status(request):
    reply = {
        "reply_to": "api_login_status",
        "username": request.user.username,
        "logged_in": request.user.is_authenticated(),
    }
    if request.user.is_authenticated():
        reply["name"] = request.user.first_name
    else:
        reply["name"] = "Prandius Guest"
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


def api_currentuser_latest_posts(request):
    reply = {
        "reply_to": "api_currentuser_latest_posts",
        "username": request.user.username,
    }
    qs = Post.objects.filter(user=request.user.pk).order_by('create_time')
    reply["posts"] = [post_data(post) for post in qs.reverse()[:20]]
    reply["count"] = qs.count()
    reply["reply"] = "OK"
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


def api_post_detail(request, post_pk):
    reply = {
        "reply_to": "api_post_detail",
        "username": request.user.username,
    }
    qs = Post.objects.filter(pk=post_pk)
    if qs:
        post = qs.first()
        reply = post_data(post) 
    else:
        reply["reply"] = "ERROR"
        reply["message"] = "Post not found"
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


class PostDetailFb(TemplateView):
    template_name = 'api/post_detail.html'
    def get_context_data(self, **kwargs):
        context = super(PostDetailFb, self).get_context_data(**kwargs)
        logger.debug(self.kwargs)
        qs = Post.objects.filter(pk=self.kwargs.get('post_pk', ''))
        if qs:
            post = qs.first()
            reply = {
                "create_date": str(post.create_time),
                "description": post.description,
                "photo_url": post.foodphoto.get_photo_url(),
                "photo_url_large": post.foodphoto.photo_url,
                "user_name": post.user.first_name,
                "permalink": post.pk,
                "reply": "OK",
                "post_id": post.pk,
                "permalink": "/index.html#/post/{0}".format(post.pk),
            }
            context['post'] = reply
        logger.debug(context)
        return context

    def get(self, request, *args, **kwargs):
        uagent = request.META.get('HTTP_USER_AGENT', '')
        post_pk = self.kwargs.get('post_pk', '')
        logger.debug("User agent: {0}".format(uagent))
        if 'facebookexternalhit' not in uagent:
            HttpResponseRedirect("/index.html#/post/{0}".format(post_pk))
        response = super(PostDetailFb, self).get(request)
        return response

