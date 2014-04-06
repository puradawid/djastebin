from django.shortcuts import render
from django.views.generic.base import View
from apps.users.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from apps.pastes.models import Paste
from django.views.generic.list import ListView

# Create your views here.

class UserDetailsView(ListView):
    model = Paste
    template_name = 'users/user_pastes.html'
    context_object_name = 'paste_list'
    paginate_by = 1
    
    def get_queryset(self):
        return Paste.objects.filter(author=User.objects.filter(username=self.kwargs['user_name']))
    
    def get_context_data(self, **kwargs):
        context = super(UserDetailsView, self).get_context_data(**kwargs)
        context['user_profile'] = User.objects.get(username=self.kwargs['user_name'])
        context['total_pastes'] = self.get_queryset().count()
        return context

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