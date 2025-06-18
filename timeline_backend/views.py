from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime
from timeline.models import File, Event, Comment, Entity, UploadedDocument
from timeline.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

@login_required
def home_view(request):
    files = File.objects.all()
    return render(request, 'home.html', {'files': files})

@login_required
def actors_view(request):
    return render(request, 'base.html')

@login_required
def entities_view(request):
    entities = Entity.objects.all()
    return render(request, 'entities.html', {'entities': entities})

@login_required
def files_view(request, slug=None):
    # Fetch all files with related events to avoid N+1 queries
    files = File.objects.filter(active=True).prefetch_related("events")
    parent_files = File.objects.filter(parent__isnull=True)

    file_data = []

    for file in files:
        events = file.events.order_by("date")
        first_event = events.first()
        last_event = events.last()
        
        if first_event and last_event:
            year_range = (first_event.date.year, last_event.date.year)
        else:
            year_range = None

        file_data.append({
            "file": file,
            "year_range": year_range,
        })

    return render(request, 'files.html', {
        'file_data': file_data,
        'parent_files': parent_files,
    })

@login_required
def file_details(request, slug):
    file = get_object_or_404(File, slug=slug)
    events = file.events.order_by("date")  

    first_event = events.first()  
    last_event = events.last()   
    
    direct_documents = file.documents.all()

    context = {
        "file": file,
        "events": events,
        "first_event": first_event,
        "last_event": last_event,
        #"documents_from_events": documents_from_events,
        'documents_from_events': file.get_documents_from_events(),
        "direct_documents": direct_documents,
    }

    return render(request, "file_details.html", context)

@login_required
def subfile_details(request, slug):
    file = get_object_or_404(File, slug=slug)
    events = file.events.order_by("date")  # sorted ascending

    first_event = events.first()  # first event or None
    last_event = events.last()    # last event or None

    context = {
        "file": file,
        "events": events,
        "first_event": first_event,
        "last_event": last_event,
    }

    if request.headers.get("Hx-Request") == "true":
        return render(request, "partials/subfile_details.html", context)

    return render(request, "subfile_details.html", context)

@login_required
def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = CommentForm()
    top_level_comments = event.comments.filter(parent__isnull=True).order_by("date")

    return render(request, 'partials/event_details_partial.html', {
        'event': event,
        'form': form,
        'comments': top_level_comments,
    })

@login_required
def add_comment(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_object = event
            comment.user = request.user
            comment.save()
            # Render only the single new comment HTML snippet
            return render(request, 'comments/comment_single.html', {'comment': comment})
    return HttpResponseBadRequest()
    
