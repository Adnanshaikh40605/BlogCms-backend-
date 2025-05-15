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
from django.http import HttpResponse, JsonResponse
from django.views.static import serve
import sys
import traceback
from django.db import connection

# Welcome page
def welcome(request):
    return HttpResponse("""
    <html>
        <head><title>Blog CMS Backend</title></head>
        <body>
            <h1>Welcome to the Blog CMS Backend</h1>
            <p>This is the API server for the Blog CMS application.</p>
            <p>Visit <a href="/debug-info/">debug-info</a> for more information.</p>
            <p>Visit <a href="/test-db/">test-db</a> to test database connection.</p>
        </body>
    </html>
    """)

# Debug info endpoint
def debug_info(request):
    try:
        # Collect debug information
        python_version = sys.version
        environment = 'Production' if not settings.DEBUG else 'Development'
        database = connection.vendor
        settings_debug = settings.DEBUG
        allowed_hosts = settings.ALLOWED_HOSTS
        
        # Return as JSON
        return JsonResponse({
            'status': 'ok',
            'python_version': python_version,
            'environment': environment,
            'database': database,
            'settings_debug': settings_debug,
            'allowed_hosts': allowed_hosts,
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error_message': str(e),
            'traceback': traceback.format_exc(),
        }, status=500)

# Test database connection
def test_db_connection(request):
    try:
        # Try to execute a simple query to test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        # Return success message
        return JsonResponse({
            'status': 'success',
            'message': 'Successfully connected to the database',
            'database_type': connection.vendor,
            'test_query_result': result[0] if result else None,
        })
    except Exception as e:
        # Return error message
        error_message = str(e)
        tb = traceback.format_exc()
        
        return JsonResponse({
            'status': 'error',
            'error_type': type(e).__name__,
            'error_message': error_message,
            'traceback': tb,
        }, status=500)

urlpatterns = [
    path('', welcome, name='welcome'),
    path('debug-info/', debug_info, name='debug_info'),
    path('test-db/', test_db_connection, name='test_db_connection'),
    path('test-db', test_db_connection, name='test_db_connection_no_slash'),  # Add version without trailing slash
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    # Add path for custom debug upload endpoint
    path('api/debug-ckeditor-upload/', include('blog.urls')),
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
