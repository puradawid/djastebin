# ./apps/pastes/views.py

# Django imports
from apps.pastes.models import Paste, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.pastes import forms
from django.http.response import Http404 
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin 
from django.views.generic.list import ListView
from datetime import timedelta
from django.utils import timezone
from django.forms.models import model_to_dict
from notifications.models import Notification
# Managing and displaying pastes views

class CreatePasteView(CreateView):
    model = Paste
    template_name = 'pastes/modify_paste.html'
    form_class = forms.PasteForm
    
    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.author = self.request.user
        return super(CreatePasteView, self).form_valid(form)
    
    def get_initial(self):
        if self.request.user.is_authenticated():
            return model_to_dict(self.request.user.account.settings)
        return super(CreatePasteView, self).get_initial()

class ReadPasteView(CreateView):
    template_name = 'pastes/paste.html'
    form_class = forms.CommentForm
    
    def get_context_data(self, **kwargs):
        origin = Paste.objects.get(pk=self.kwargs['pk'])
        context = super(ReadPasteView, self).get_context_data(**kwargs)
        context['paste'] = origin
        self.increment_hits(origin)
        if origin.visibility == 'PRIVATE':
            if not origin.author == self.request.user:
                raise PermissionDenied       
        context['nodes'] = Comment.objects.filter(paste=Paste.objects.get(pk=self.kwargs['pk']))
        if self.request.user.is_authenticated():
            Notification.objects.filter(recipient=self.request.user, target_object_id=origin.pk).mark_all_as_read()
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.paste = Paste.objects.get(pk=self.kwargs['pk'])
        return super(ReadPasteView, self).form_valid(form)

    def increment_hits(self, paste):
        if paste.pk not in self.request.session: 
            paste.hits += 1
            paste.save()
            self.request.session[paste.pk] = 1

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
        obj = super(DeletePasteView, self).get_object(*args, **kwargs)
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
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        return Paste.objects.filter(visibility='PUBLIC', created__range=[start_date, end_date]).order_by('-hits', '-created')

    def get_context_data(self, **kwargs):
        context = super(TrendingPastesView, self).get_context_data(**kwargs)
        context.update({
            'days': self.kwargs['days'],
        })
        return context
