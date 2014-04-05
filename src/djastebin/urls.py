from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps import users, pastes

urlpatterns = patterns('',
    url(r'^', include('apps.pastes.urls')),
    url(r'^u/', include('apps.users.urls')),
    url(r'^settings/$', users.views.SettingsView.as_view(), name='settings'),
    url(r'^profile/$', users.views.ProfileView.as_view(), name='profile'),
    url(r'^login/$', users.views.LoginView.as_view(), name='login'),
    url(r'^logout/$', users.views.LogoutView.as_view(), name='logout'),
    url(r'^registration/$', users.views.RegistrationView.as_view(), name='registration'),
    url(r'^trends/$', pastes.views.TrendingPastesView.as_view(), name='trends'),
    url(r'^admin/', include(admin.site.urls)),
)
