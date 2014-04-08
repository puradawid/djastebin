# ./apps/pastes/views.py

# Django imports
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from apps.pastes.models import Paste, Comment
from apps.pastes.forms import PasteForm, CommentForm
from django.http.response import HttpResponseRedirect

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

class ReadPasteView(View):
    def get(self, request, paste_id):
        form = CommentForm()
        return render(request, 'pastes/paste.html', {'nodes': Comment.objects.all(), 'form': form})
    def post(self, request, paste_id):
        form = CommentForm(request.POST)
        if (form.is_valid()):
            author = request.user
            paste = Paste.objects.get(id=1)
            parent = Comment.objects.get(id=id_parent)
            form.save()
            return HttpResponseRedirect('/paste')
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
