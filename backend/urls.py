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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.static import serve
from blog.comment_api import comment_counts_direct

# Welcome page
def welcome(request):
    return HttpResponse("""
    <html>
        <head><title>Blog CMS Backend</title></head>
        <body>
            <h1>Welcome to the Blog CMS Backend</h1>
            <p>This is the API server for the Blog CMS application.</p>
        </body>
    </html>
    """)

urlpatterns = [
    path('', welcome, name='welcome'),
    path('admin/', admin.site.urls),
    
    # Direct access to the comments counts endpoint
    path('api/comments/counts/', comment_counts_direct, name='direct-comment-counts'),
    
    # Include blog URLs with API prefix
    path('api/', include('blog.urls')),
    
    # CKEditor URLs
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Add this to serve CKEditor 5 media files in development
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
# For production media serving (not recommended for high-traffic sites, but works for demos)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
