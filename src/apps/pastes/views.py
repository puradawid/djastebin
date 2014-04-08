# ./apps/pastes/views.py

# Django imports
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View, CreateView
from apps.pastes.models import Paste, Comment
from apps.pastes.forms import PasteForm

# Managing and displaying pastes views

class CreatePasteView(View):

    def get(self, request):
	form = PasteForm()
        return render(request, 'pastes/create_paste.html', {'form' : form })

    def post(self, request):
	form = PasteForm(request.POST) 	
	if form.is_valid():
		paste = form.save()
		return redirect(reverse('paste_id', args=[paste.id])) 
	return render(request, 'pastes/create_paste.html', {'form' : form })

class ShowPasteCreateCommentView(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'pastes/paste.html'

    def valid_form(self, form):
        form.instance.paste = Paste.objects.get(id=self.kwargs['paste_id'])  #set owner, paste, etc
	return super(ShowPasteCreateCommentView, self).valid_form(form)

    def get_context_data(self, **kwargs):
        origin = Paste.objects.get(id=self.kwargs['paste_id'])
        context = super(CreateView, self).get_context_data(**kwargs)
	context['paste'] = origin
	return context
    

class ReadPasteView(View):
    def get(self, request, paste_id):
        return render(request, 'pastes/paste.html')
    def post(self, request, paste_id):
        return render(request, 'pastes/paste.html')
    
class UpdatePasteView(View):
    def get(self, request, paste_id):
        return render(request, 'home/index.html')
    def post(self, request, paste_id):
        return render(request, 'home/index.html')
    
class DeletePasteView(View):
    def get(self, request, paste_id):
        return render(request, 'home/index.html')
    def post(self, request, paste_id):
        return render(request, 'home/index.html')
    
class TrendingPastesView(View):
    def get(self, request, paste_id):
        return render(request, 'home/index.html')
    def post(self, request, paste_id):
        return render(request, 'home/index.html')
