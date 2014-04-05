from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.

def login(request):
    return render(request, 'users/user.html', {'user_name' : 'login'})

def register(request):
    return render(request, 'users/user.html', {'user_name' : 'register'})

class UserDetailsView(View):
    def get(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : user_name})
    def post(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : user_name})
    
class SettingsView(View):
    def get(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'settings_get'})
    def post(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'settings_post'})

class ProfileView(View):
    def get(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'profile'})
    def post(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'profile'})

class LoginView(View):
    def get(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'login'})
    def post(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'login'})
    
class LogoutView(View):
    def get(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'logout'})
    def post(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'logout'})

class RegistrationView(View):
    def get(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'login'})
    def post(self, request, user_name):
        return render(request, 'users/user.html', {'user_name' : 'login'})