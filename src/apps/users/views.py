from django.shortcuts import render
from django.views.generic.base import View
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from apps.pastes.models import Paste
from django.views.generic.list import ListView
# Create your views here.

class UserDetailsView(ListView):
    model = Paste
    template_name = 'users/user_pastes.html'
    context_object_name = 'paste_list'
    paginate_by = 10
    
    def get_queryset(self):
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
    
    def get(self, *args, **kwargs):
        try:
            self.user_profile = User.objects.get(username=kwargs['user_name'])
        except User.DoesNotExist:
            return HttpResponseRedirect("/")
        return super(UserDetailsView, self).get(*args, **kwargs);

class SettingsView(View):
    def get(self, request):
        return render(request, 'users/user.html', {'user_name' : 'settings_get'})
    def post(self, request):
        return render(request, 'users/user.html', {'user_name' : 'settings_post'})

class ProfileView(View):
    def get(self, request):
        return render(request, 'users/user.html', {'user_name' : 'profile'})
    def post(self, request):
        return render(request, 'users/user.html', {'user_name' : 'profile'})