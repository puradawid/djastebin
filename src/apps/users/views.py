from django.shortcuts import render, redirect
from django.views.generic.base import View
from apps.users.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

class UserDetailsView(View):
    def get(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : user_name})
    def post(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : user_name})
    
class SettingsView(View):
    def get(self, request):
        return render(request, 'users/user.html', {'user_name' : 'settings_get'})
    def post(self, request):
        return render(request, 'users/user.html', {'user_name' : 'settings_post'})

class ProfileView(View):
    def get(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'profile'})
    def post(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'profile'})

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