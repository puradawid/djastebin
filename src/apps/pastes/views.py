from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class CreatePasteView(View):
    def get(self, request):
        return render(request, 'home/index.html')
    def post(self, request):
        return render(request, 'home/index.html')

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