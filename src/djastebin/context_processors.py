from apps.pastes.models import Paste

def recent_pastes(request):
    return { 'recent_pastes' : Paste.objects.order_by('-created')[:5] }