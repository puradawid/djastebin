from django.shortcuts import render
from django.views.generic.base import View
from apps.users.forms import ProfileEditForm, SettingsChangeForm
from apps.pastes.models import Paste
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect, Http404
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from braces.views._access import LoginRequiredMixin
from django.core.urlresolvers import reverse
from apps.users.models import Settings

# Create your views here.

class UserDetailsView(ListView):
    model = Paste
    template_name = 'users/user_pastes.html'
    context_object_name = 'paste_list'
    paginate_by = 10
    
    def get_queryset(self):
        
        try:
            self.user_profile = User.objects.get(username=self.kwargs['user_name'])
        except User.DoesNotExist:
            raise Http404
        
        if self.request.user.is_authenticated(): 
            return Paste.objects.filter(author=self.user_profile).order_by('-created')
        return Paste.objects.filter(author=self.user_profile, visibility='PUBLIC').order_by('-created')
    
    def get_context_data(self, **kwargs):
        context = super(UserDetailsView, self).get_context_data(**kwargs)
        context.update({
            'user_profile': self.user_profile,
            'total_pastes': self.get_queryset().count(),
        })
        return context

class SettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Settings
    template_name = 'users/settings.html'
    success_url = '.'
    success_message = 'Your settins has been updated!'
    
    def get_object(self, *args, **kwargs):
        return self.request.user.account.settings;
    
class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = ProfileEditForm
    success_url = '.'
    success_message = 'Your profile has been updated!'
    
    def get_object(self, *args, **kwargs):
        return self.request.user;