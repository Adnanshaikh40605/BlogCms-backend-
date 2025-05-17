from django.http import JsonResponse
from rest_framework.decorators import api_view
import logging
from .models import Comment

# Setup logger
logger = logging.getLogger(__name__)

@api_view(['GET'])
def comment_counts_direct(request):
    """Get counts for comments in different states - direct access endpoint"""
    try:
        # Log the request for debugging
        logger.info(f"Direct access to comment_counts_direct endpoint: {request.path}")
        
        # Force evaluate the counts to ensure they're accurate
        all_count = Comment.objects.filter(is_trash=False).count()
        pending_count = Comment.objects.filter(approved=False, is_trash=False).count()
        approved_count = Comment.objects.filter(approved=True, is_trash=False).count()
        trash_count = Comment.objects.filter(is_trash=True).count()
        
        # Log counts for debugging
        logger.info(f"Direct count method: all={all_count}, pending={pending_count}, approved={approved_count}, trash={trash_count}")
        
        response_data = {
            'all': all_count,
            'pending': pending_count,
            'approved': approved_count,
            'trash': trash_count,
            'status': 'success',
            'message': 'Comment counts retrieved successfully (direct method)',
            'path': request.path
        }
        
        # Return the response
        logger.info(f"Returning direct comment counts: {response_data}")
        return JsonResponse(response_data)
    except Exception as e:
        logger.error(f"Error getting direct comment counts: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e), 'detail': 'An error occurred while fetching comment counts'}, status=500) 