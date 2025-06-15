from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView
from timeline.forms import TailwindLoginForm

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard', views.home_view, name='home'),
    path('files/', views.files_view, name='files'),
    path('actors/', views.files_view, name='actors'),
    path('stages/', views.files_view, name='stages'),
    path('assets/', views.files_view, name='assets'),
    path('acts/', views.files_view, name='acts'),
    path('scripts/', views.files_view, name='scripts'),
    path('documents/', views.files_view, name='documents'),
    path('logout/', views.files_view, name='logout'),
    path('files/<slug:slug>/', views.file_details, name='file_details'),
    path('subfile/<slug:slug>/', views.subfile_details, name='subfile_details'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=TailwindLoginForm
    ), name='login'),
    path('event/<int:event_id>/', views.event_details, name='event_details'),
    path('event/<int:event_id>/comment/add/', views.add_comment, name='add_comment'),
    path('comments/add/event/<int:event_id>/', views.add_comment, name='add_comment_event'),
    path('comments/add/file/<int:file_id>/', views.add_comment, name='add_comment_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)