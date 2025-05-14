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

# Diagnostic view to help troubleshoot issues
def debug_info(request):
    try:
        # Get system info
        debug_data = {
            "python_version": sys.version,
            "settings_debug": settings.DEBUG,
            "allowed_hosts": settings.ALLOWED_HOSTS,
            "database": settings.DATABASES['default']['ENGINE'],
            "request_meta": {k: str(v) for k, v in request.META.items() if k.startswith('HTTP_')},
            "request_path": request.path,
            "request_method": request.method,
            "cors_settings": {
                "allow_all_origins": getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False),
                "allowed_origins": getattr(settings, 'CORS_ALLOWED_ORIGINS', []),
                "allow_credentials": getattr(settings, 'CORS_ALLOW_CREDENTIALS', False),
            }
        }
        return JsonResponse(debug_data)
    except Exception as e:
        error_info = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        return JsonResponse(error_info, status=500)

# New endpoint to test database connection
def test_db_connection(request):
    try:
        # Try to make a simple database query
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
        
        # Test more complex queries to diagnose issues
        try:
            # Try to list tables in the database
            with connection.cursor() as cursor:
                if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema='public' AND table_type='BASE TABLE'
                        LIMIT 5
                    """)
                    tables = [row[0] for row in cursor.fetchall()]
                else:
                    tables = ["Non-PostgreSQL database detected"]
        except Exception as table_error:
            tables = [f"Error listing tables: {str(table_error)}"]
        
        # Get database connection info (sanitized)
        db_info = {
            "engine": settings.DATABASES['default']['ENGINE'],
            "name": settings.DATABASES['default']['NAME'],
            "host": settings.DATABASES['default'].get('HOST', 'Not specified'),
            "port": settings.DATABASES['default'].get('PORT', 'Not specified'),
            "user": settings.DATABASES['default'].get('USER', 'Not specified'),
            # Don't include password for security reasons
            "options": settings.DATABASES['default'].get('OPTIONS', {}),
        }
        
        return JsonResponse({
            "status": "success",
            "message": "Database connection successful",
            "connection_info": db_info,
            "sample_tables": tables,
            "query_result": row[0] if row else None
        })
    except Exception as e:
        error_info = {
            "status": "error",
            "error_message": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "db_settings": {
                "engine": settings.DATABASES['default']['ENGINE'],
                "name": settings.DATABASES['default']['NAME'],
                "host": settings.DATABASES['default'].get('HOST', 'Not specified'),
                "port": settings.DATABASES['default'].get('PORT', 'Not specified'),
                "user": settings.DATABASES['default'].get('USER', 'Not specified'),
                # Don't include password for security reasons
            }
        }
        
        # Try to get more specific database error information for common issues
        error_str = str(e).lower()
        if "timeout" in error_str:
            error_info["possible_cause"] = "Connection timeout. The database server might be unreachable or blocked by a firewall."
        elif "authentication" in error_str or "password" in error_str:
            error_info["possible_cause"] = "Authentication failed. Check your database credentials."
        elif "does not exist" in error_str:
            error_info["possible_cause"] = "Database or schema doesn't exist. Check your database name."
        elif "permission denied" in error_str:
            error_info["possible_cause"] = "Permission issue. The user doesn't have sufficient privileges."
        elif "too many connections" in error_str:
            error_info["possible_cause"] = "The database has reached its connection limit."
        
        return JsonResponse(error_info, status=500)

# A simple view for the root URL
def welcome(request):
    try:
        # Build a super-simple response for troubleshooting
        basic_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Blog CMS API</title>
            <style>
                body { font-family: sans-serif; max-width: 800px; margin: 20px auto; padding: 20px; }
                h1 { color: #2c3e50; }
            </style>
        </head>
        <body>
            <h1>Blog CMS API</h1>
            <p>Welcome to the Blog CMS API. This is a minimal page for troubleshooting.</p>
            <p>Available Endpoints:</p>
            <ul>
                <li><a href="/admin/">/admin/</a> - Django Admin</li>
                <li><a href="/api/">/api/</a> - API</li>
                <li><a href="/debug-info/">/debug-info/</a> - Diagnostic Info</li>
            </ul>
        </body>
        </html>
        """
        return HttpResponse(basic_html, content_type='text/html')
    except Exception as e:
        # Super simple error response
        error_text = f"Error: {str(e)}"
        return HttpResponse(error_text, content_type='text/plain', status=500)

urlpatterns = [
    path('', welcome, name='welcome'),
    path('debug-info/', debug_info, name='debug_info'),
    path('test-db/', test_db_connection, name='test_db_connection'),
    path('test-db', test_db_connection, name='test_db_connection_no_slash'),  # Add version without trailing slash
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
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
