from django.shortcuts import render
from django.views.generic.base import View
from apps.users.forms import ProfileEditForm, SettingsChangeForm
from apps.pastes.models import Paste
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect

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
    SUCCESS_SESSION_KEY = 'settings_change_success'
    
    def get(self, request):
        success = None
        if self.SUCCESS_SESSION_KEY in request.session:
            success = request.session[self.SUCCESS_SESSION_KEY]
            del request.session[self.SUCCESS_SESSION_KEY]
        return render(request, 'users/settings.html', {'form' : SettingsChangeForm(instance=request.user.account.settings), 'success': success})
    def post(self, request):
        form = SettingsChangeForm(request.POST, instance=request.user.account.settings)
        if form.is_valid():
            default_syntax = form.clean_default_syntax()
            default_visibility = form.clean_default_visibility()
            default_expiration = form.clean_default_expiration()
            form.save()
            if self.SUCCESS_SESSION_KEY not in request.session:
                request.session[self.SUCCESS_SESSION_KEY] = 'Your settings has been updated!'
                return HttpResponseRedirect('/settings')
        return render(request, 'users/settings.html', {'form': form})

class ProfileView(View):
    SUCCESS_SESSION_KEY = 'profile_edit_success'
    
    def get(self, request):
        success = None
        if self.SUCCESS_SESSION_KEY in request.session:
            success = request.session[self.SUCCESS_SESSION_KEY]
            del request.session[self.SUCCESS_SESSION_KEY]
        return render(request, 'users/profile.html', {'form' : ProfileEditForm(instance=request.user), 'success': success})
    def post(self, request):
        user = request.user
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            email = form.clean_email()
            first_name = form.clean_first_name()
            last_name = form.clean_last_name()
            password = form.clean_password()
            form.save()
            if self.SUCCESS_SESSION_KEY not in request.session:
                request.session[self.SUCCESS_SESSION_KEY] = 'Your profile has been updated!'
            return HttpResponseRedirect("/profile")
        return render(request, 'users/profile.html', {'form' : form})