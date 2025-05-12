"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# A simple view for the root URL
def welcome(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blog CMS API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #2c3e50;
            }
            .endpoint {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            a {
                color: #3498db;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Blog CMS API</h1>
        <p>Welcome to the Blog CMS API. This is the backend service for the Blog Content Management System.</p>
        
        <h2>Available Endpoints:</h2>
        <div class="endpoint">
            <strong>Admin:</strong> <a href="/admin/">/admin/</a> - Django Admin Interface
        </div>
        <div class="endpoint">
            <strong>API:</strong> <a href="/api/">/api/</a> - API Endpoints
        </div>
        <div class="endpoint">
            <strong>CKEditor:</strong> <a href="/ckeditor/">/ckeditor/</a> - CKEditor Uploads
        </div>
        
        <p>For more details about the API endpoints, please refer to the documentation.</p>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', welcome, name='welcome'),
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
