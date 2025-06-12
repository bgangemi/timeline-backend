from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

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
    path('login/', auth_views.LoginView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)