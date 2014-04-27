from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^(?P<user_name>[\w._-]+)/$', views.UserDetailsView.as_view(), name='user')
)
