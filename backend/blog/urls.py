from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from . import views
from django.views.decorators.csrf import csrf_exempt
from django_ckeditor_5.views import upload
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
# Add routers here if needed

urlpatterns = [
    # Add custom debug endpoint for CKEditor uploads
    path('debug-ckeditor-upload/', views.debug_ckeditor_upload, name='debug_ckeditor_upload'),
]

# Add router paths
urlpatterns += router.urls 