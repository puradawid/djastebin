# ./apps/pastes/views.py

# Django imports
from django.shortcuts import render
from django.views.generic import View
from apps.pastes.models import Paste
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.pastes import forms
from django.http.response import Http404
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin 
# Managing and displaying pastes views

class CreatePasteView(CreateView):
    model = Paste
    template_name = 'pastes/modify_paste.html'
    form_class = forms.PasteForm
    
    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.author = self.request.user
        return super(CreatePasteView, self).form_valid(form)

class ReadPasteView(View):
    def get(self, request, pk):
        return render(request, 'home/index.html')
    def post(self, request, pk):
        return render(request, 'home/index.html')

class UpdatePasteView(LoginRequiredMixin, UpdateView):
    model = Paste
    template_name = 'pastes/modify_paste.html'
    form_class = forms.PasteFormEdit
    
    def get_object(self, *args, **kwargs):
        obj = super(UpdatePasteView, self).get_object(*args, **kwargs)
        if not obj.author == self.request.user:
            raise Http404
        return obj
    
class DeletePasteView(LoginRequiredMixin, DeleteView):
    model = Paste
    template_name = 'pastes/delete_paste.html'
    
    def get_object(self, *args, **kwargs):
        obj = super(UpdatePasteView, self).get_object(*args, **kwargs)
        if not obj.author == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('user', args=[self.request.user.username])
    
class TrendingPastesView(View):
    def get(self, request, paste_id):
        return render(request, 'home/index.html')
    def post(self, request, paste_id):
        return render(request, 'home/index.html')
