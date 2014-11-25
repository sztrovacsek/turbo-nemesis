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
