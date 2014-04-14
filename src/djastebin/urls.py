from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django_common.decorators import anonymous_required
import django.contrib.auth.views
from django.views.generic.edit import CreateView
from apps.users.forms import UserRegistrationForm
import apps.pastes.views
import apps.users.views
import notifications
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^notifications/', include(notifications.urls)),
    url(r'^settings/$', login_required(apps.users.views.SettingsView.as_view()), name='settings'),
    url(r'^profile/$', apps.users.views.ProfileView.as_view(), name='profile'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^login/$', anonymous_required(django.contrib.auth.views.login), {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^registration/$', anonymous_required(CreateView.as_view(
            template_name='users/registration.html',
            form_class=UserRegistrationForm,
            success_url='/login/'
    )), name='registration'),
    url(r'^password/', include('password_reset.urls')),
    url(r'^trends/$', apps.pastes.views.TrendingPastesView.as_view(), name='trends', kwargs={'days' : '1'}),
    url(r'^trends/(?P<days>1|7|30|365|all)/$', apps.pastes.views.TrendingPastesView.as_view(), name='trends_by_day'),
    url(r'^u/', include('apps.users.urls')),
    url(r'^', include('apps.pastes.urls')),
    url(r'', include('social_auth.urls')),
)