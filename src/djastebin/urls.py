from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib import admin
admin.autodiscover()

import apps.pastes.views
import apps.users.views
#from apps.users.views import *

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^settings/$', login_required(apps.users.views.SettingsView.as_view()), name='settings'),
    url(r'^profile/$', login_required(apps.users.views.ProfileView.as_view()), name='profile'),
    url(r'^login/$', apps.users.views.LoginView.as_view(), name='login'),
    url(r'^logout/$', apps.users.views.LogoutView.as_view(), name='logout'),
    url(r'^registration/$', apps.users.views.RegistrationView.as_view(), name='registration'),
    url(r'^trends/$', apps.pastes.views.TrendingPastesView.as_view(), name='trends'),
    url(r'^u/', include('apps.users.urls')),
    url(r'^', include('apps.pastes.urls')),
)
