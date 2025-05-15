from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import json
import traceback

# Debug endpoint for CKEditor uploads
@csrf_exempt
def debug_ckeditor_upload(request):
    """
    Debug endpoint for CKEditor uploads to diagnose issues
    """
    if request.method == 'POST':
        try:
            # Check if upload file exists in request
            if 'upload' not in request.FILES:
                return JsonResponse({
                    'error': {
                        'message': 'No file uploaded. Expected file with name "upload"',
                        'received_fields': list(request.POST.keys()),
                        'files_received': list(request.FILES.keys())
                    }
                }, status=400)
            
            upload = request.FILES['upload']
            
            # Check file details
            file_details = {
                'name': upload.name,
                'size': upload.size,
                'content_type': upload.content_type,
            }
            
            # Check if media directory exists
            media_root = settings.MEDIA_ROOT
            uploads_dir = os.path.join(media_root, 'uploads')
            
            directory_status = {
                'media_root_exists': os.path.exists(media_root),
                'media_root_path': media_root,
                'uploads_dir_exists': os.path.exists(uploads_dir),
                'uploads_dir_path': uploads_dir,
            }
            
            # Try to create directories if they don't exist
            if not os.path.exists(media_root):
                try:
                    os.makedirs(media_root)
                    directory_status['media_root_created'] = True
                except Exception as e:
                    directory_status['media_root_error'] = str(e)
            
            if not os.path.exists(uploads_dir):
                try:
                    os.makedirs(uploads_dir)
                    directory_status['uploads_dir_created'] = True
                except Exception as e:
                    directory_status['uploads_dir_error'] = str(e)
            
            # Try to save the file
            save_path = os.path.join(uploads_dir, upload.name)
            save_status = {'attempted_path': save_path}
            
            try:
                with open(save_path, 'wb+') as destination:
                    for chunk in upload.chunks():
                        destination.write(chunk)
                save_status['success'] = True
            except Exception as e:
                save_status['error'] = str(e)
                save_status['traceback'] = traceback.format_exc()
            
            # If successfully saved, return URL
            if save_status.get('success'):
                url = f"{settings.MEDIA_URL}uploads/{upload.name}"
                return JsonResponse({
                    'url': url,
                    'debug_info': {
                        'file': file_details,
                        'directories': directory_status,
                        'save': save_status
                    }
                })
            else:
                # Return detailed error
                return JsonResponse({
                    'error': {
                        'message': 'Failed to save uploaded file',
                        'file': file_details,
                        'directories': directory_status,
                        'save': save_status
                    }
                }, status=500)
                
        except Exception as e:
            # Return any unexpected errors
            return JsonResponse({
                'error': {
                    'message': f'Upload error: {str(e)}',
                    'traceback': traceback.format_exc()
                }
            }, status=500)
    
    # Return method not allowed for non-POST requests
    return JsonResponse({
        'error': {
            'message': f'Method {request.method} not allowed'
        }
    }, status=405) 