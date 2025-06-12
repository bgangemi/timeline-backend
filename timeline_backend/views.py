from django.shortcuts import render, get_object_or_404
from timeline.models import File
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    files = File.objects.all()
    return render(request, 'base.html', {'files': files})

def files_view(request, slug=None):
    files = File.objects.all()
    parent_files = File.objects.filter(parent__isnull=True)
    return render(request, 'files.html', {
        'files': files,
        'parent_files': parent_files
    })

@login_required
def file_details(request, slug):
    file = get_object_or_404(File, slug=slug)
    return render(request, "file_details.html", {"file": file})

@login_required
def subfile_details(request, slug):
    file = get_object_or_404(File, slug=slug)

    if request.headers.get("Hx-Request") == "true":
        return render(request, "partials/subfile_details.html", {"file": file})

    return render(request, "subfile_details.html", {"file": file})