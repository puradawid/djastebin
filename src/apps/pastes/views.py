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
from django.views.generic.list import ListView
from django.utils.datetime_safe import datetime
from datetime import timedelta
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
    
class TrendingPastesView(ListView):
    template_name = 'pastes/trends.html'
    context_object_name = 'paste_list'
    paginate_by = 10
    
    def get_queryset(self):
        
        if self.kwargs['days'] == 'all':
            return Paste.objects.filter(visibility='PUBLIC').order_by('-hits', '-created')
        days = int(self.kwargs['days'])
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return Paste.objects.filter(visibility='PUBLIC', created__range=[start_date, end_date]).order_by('-hits', '-created')

    def get_context_data(self, **kwargs):
        context = super(TrendingPastesView, self).get_context_data(**kwargs)
        context.update({
            'days': self.kwargs['days'],
        })
        return context
