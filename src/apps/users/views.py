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

class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = ProfileEditForm
    success_url = '/profile/'
    success_message = 'Your profile has been updated!'
    
    def get_object(self, *args, **kwargs):
        return self.request.user;
    
    def get_success_url(self):
        return reverse('profile')