# ./apps/pastes/views.py

# Django imports
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from apps.pastes.models import Paste
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

class ReadPasteView(View):
    def get(self, request, paste_id):
        return render(request, 'home/index.html')
    def post(self, request, paste_id):
        return render(request, 'home/index.html')
    
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
