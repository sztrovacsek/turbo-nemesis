from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', auth_views.login,
        {'template_name': 'api/login.html'}),

    url(r'^$', RedirectView.as_view(url='/index.html', permanent=False), name='index-view'),
)
