from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from ckeditor.fields import RichTextField

APPROXIMATENESS_LEVELS = [
    ('none', 'Exact'),
    ('day', 'Approximate day'),
    ('week', 'Approximate week'),
    ('month', 'Approximate month'),
    ('year', 'Approximate year'),
    ('unknown', 'Unknown/very vague'),
]

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comment = RichTextField(blank=False, null=False)  # better to require comment
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
    # Check if content_type and object_id are valid
        if self.content_type_id and self.object_id:
            try:
                target = self.content_object  # Try to get related object
            except Exception:
                target = None
        else:
            target = None

        user_str = str(self.user) if self.user else "Anonymous"
        return f"Comment by {user_str} on {target if target else 'Unknown content'}"

class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="files")
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    name = models.CharField(max_length=200, unique=True)
    summary = RichTextField(blank=True, null=True)
    details = RichTextField(blank=True, null=True)
    information = RichTextField(blank=True, null=True, verbose_name="Practical informations") 
    created_at = models.DateTimeField(auto_now_add=True)
    documents = GenericRelation('UploadedDocument')
    notes = RichTextField(blank=True, null=True) 
    comments = GenericRelation(Comment)
    tags = models.ManyToManyField('Tag', blank=True, related_name='file')

    def __str__(self):
        return self.name

class AbuseType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")
    file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")
    name = models.CharField(max_length=200)
    date = models.DateField()
    date_approx_level = models.CharField(
        max_length=10,
        choices=APPROXIMATENESS_LEVELS,
        default='none',
    )
    description = RichTextField(blank=True, null=True)
    details = RichTextField(blank=True, null=True)
    abuse_types = models.ManyToManyField(AbuseType, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    documents = GenericRelation('UploadedDocument')
    comments = GenericRelation(Comment)
    tags = models.ManyToManyField('Tag', blank=True, related_name='event')

    def get_absolute_url(self):
        return reverse('event_details', kwargs={'event_id': self.id})

    def __str__(self):
        return f"{self.date}: {self.name} ({self.file.name})" if self.file else f"{self.date}: {self.name}"

    class Meta:
        ordering = ["date"]

class UploadedDocument(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    document = models.FileField(upload_to="documents/")
    description = RichTextField(blank=True, null=True) 
    uploaded_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(blank=True, null=True)
    date_approx_level = models.CharField(
        max_length=10,
        choices=APPROXIMATENESS_LEVELS,
        default='none',
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name='uploaded_document')

    def __str__(self):
        return f"Document for {self.content_object}"