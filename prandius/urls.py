from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

from api.views import *


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', auth_views.login,
        {'template_name': 'admin/login.html'}),

    url(r'^api/backend_login/$', api_backend_login),
    url(r'^api/test/$', api_test),
    url(r'^api/user_login_status/$', api_user_login_status),
    url(r'^sign_s3/$', api_sign_s3, name='sign-s3'),
    url(r'^api/photo_add/$', api_photo_add),
    url(r'^api/latest_posts/$', api_latest_posts),
    url(
        r'^api/currentuser/latest_posts/$',
        api_currentuser_latest_posts
    ),

    url(r'^$', RedirectView.as_view(url='/index.html', permanent=False), name='index-view'),

)
