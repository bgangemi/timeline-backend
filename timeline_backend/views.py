from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime
from timeline.models import File, Event, Comment
from timeline.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

@login_required
def home_view(request):
    files = File.objects.all()
    return render(request, 'base.html', {'files': files})

@login_required
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
    events = file.events.order_by("date")  # sorted ascending

    first_event = events.first()  # first event or None
    last_event = events.last()    # last event or None

    context = {
        "file": file,
        "events": events,
        "first_event": first_event,
        "last_event": last_event,
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
    
