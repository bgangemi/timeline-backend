from django.shortcuts import render
from timeline.models import File

def home_view(request):
    files = File.objects.all()

    return render(request, 'base.html', {'files': files})