from django.shortcuts import render, redirect
from django.views.generic.base import View
from apps.users.forms import UserRegistrationForm, ProfileEditForm, SettingsChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from apps.users.models import Settings, Account

# Create your views here.

class UserDetailsView(View):
    def get(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : user_name})
    def post(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : user_name})
    
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

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html', {'form' : AuthenticationForm()})
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
        return render(request, 'users/login.html', {'form' : form})
    
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
        return HttpResponseRedirect("/")

class RegistrationView(View):
    def get(self, request):
        return render(request, 'users/registration.html', {'form' : UserRegistrationForm()})
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password2()
            form.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return HttpResponseRedirect("../")
        return render(request, 'users/registration.html', {'form' : form})