# ./apps/pastes/views.py

# Django imports
from django.shortcuts import render, redirect
from django.views.generic import View
from apps.pastes.models import Paste

# Utility imports
from datetime import timedelta, date

# Managing and displaying pastes views

class CreatePasteView(View):
    def get(self, request):
        return render(request, 'pastes/create_paste.html')
    def post(self, request):
	#retrieve data
	title = request.POST["name"]
	expire_date = request.POST["expiration"]
	content = request.POST["content"]
	visibility = request.POST["visibility"]
	syntax = request.POST["syntax"]
		
	if expire_date == "0":      # if expire date is never 
		expire_date = None  # put null into variable
	else:                       # else calculate a date of expire
		expire_date = date.today() + timedelta(minutes=int(expire_date))        

	if not request.user.is_anonymous(): 
		user = request.user
	else:
		user = None   	    # IMPORTANT: user can be null!
	#paste creation
	paste = Paste.objects.create(title=title, expire_date=expire_date, content=content, visibility = visibility, author=user)	
	
	return redirect(str(paste.id) + "/") 

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
