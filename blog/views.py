from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
import logging
from django.http import JsonResponse
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

from .models import BlogPost, BlogImage, Comment
from .serializers import (
    BlogPostSerializer, 
    BlogPostListSerializer, 
    BlogImageSerializer, 
    CommentSerializer
)

# Setup logger
logger = logging.getLogger(__name__)

class BlogPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing blog posts.
    
    list:
    Return a list of all blog posts.
    
    retrieve:
    Return a specific blog post by ID.
    
    create:
    Create a new blog post.
    
    update:
    Update an existing blog post.
    
    partial_update:
    Partially update an existing blog post.
    
    destroy:
    Delete a blog post.
    """
    queryset = BlogPost.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            # Filter by published status for list view
            published = self.request.query_params.get('published')
            if published is not None:
                if published.lower() == 'true':
                    queryset = queryset.filter(published=True)
                elif published.lower() == 'false':
                    queryset = queryset.filter(published=False)
        
        # Optimize with prefetch_related
        if self.action == 'retrieve':
            # For single post view, prefetch related images and approved comments
            queryset = queryset.prefetch_related(
                'images',
                Prefetch(
                    'comments',
                    queryset=Comment.objects.filter(approved=True),
                    to_attr='approved_comments'
                )
            )
        elif self.action == 'list':
            # For list view, just prefetch images
            queryset = queryset.prefetch_related('images')
            
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a new blog post, handling both JSON and multipart requests"""
        logger.info(f"Creating blog post with content type: {request.content_type}")
        
        # Log request data for debugging
        logger.debug(f"Request data: {request.data}")
        
        # Extract additional images from form data if present
        additional_images = []
        additional_image_keys = [key for key in request.data.keys() if key.startswith('additional_images[')]
        
        if additional_image_keys:
            logger.info(f"Found additional image keys: {additional_image_keys}")
            for key in additional_image_keys:
                additional_images.append(request.data[key])
            
            # Create a mutable copy of the request data
            data = request.data.copy()
            
            # Remove the individual image fields
            for key in additional_image_keys:
                del data[key]
            
            # Add the collected images as a list
            if additional_images:
                data._mutable = True
                data['additional_images'] = additional_images
                data._mutable = False
                
            # Update the request data
            request._full_data = data
        
        # Continue with normal processing
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_images(self, request, pk=None):
        """Upload additional images to a blog post"""
        post = self.get_object()
        images = request.FILES.getlist('images')
        
        if not images:
            return Response(
                {'error': 'No images provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_images = []
        for image in images:
            blog_image = BlogImage.objects.create(post=post, image=image)
            created_images.append(BlogImageSerializer(blog_image).data)
        
        return Response(created_images, status=status.HTTP_201_CREATED)

class BlogImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing blog images.
    """
    queryset = BlogImage.objects.all()
    serializer_class = BlogImageSerializer
    parser_classes = [MultiPartParser, FormParser]

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing blog comments.
    
    list:
    Return a list of all comments.
    
    retrieve:
    Return a specific comment by ID.
    
    create:
    Create a new comment.
    
    update:
    Update an existing comment.
    
    partial_update:
    Partially update an existing comment.
    
    destroy:
    Delete a comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        # Filter by post ID
        post = self.request.query_params.get('post')
        if post is not None:
            queryset = queryset.filter(post=post)
            
        # Filter by approval status
        approved = self.request.query_params.get('approved')
        if approved is not None:
            if approved.lower() == 'true':
                queryset = queryset.filter(approved=True)
                logger.info(f"Filtering for APPROVED comments only for post {post}")
            elif approved.lower() == 'false':
                queryset = queryset.filter(approved=False)
                logger.info(f"Filtering for UNAPPROVED comments only for post {post}")
                
        # Log the query for debugging
        logger.debug(f"Comment queryset filters: post={post}, approved={approved}")
        logger.debug(f"Comment queryset SQL: {str(queryset.query)}")
        count = queryset.count()
        logger.debug(f"Comment queryset count: {count}")
        
        # Additional logging for debugging
        if count == 0 and approved == 'true':
            # If we're looking for approved comments but found none, log all comments for this post
            all_comments = Comment.objects.filter(post=post)
            approved_count = all_comments.filter(approved=True).count()
            logger.info(f"Found {approved_count} approved comments out of {all_comments.count()} total for post {post}")
            
            # Log the first few comments with their approval status for debugging
            for comment in all_comments[:5]:
                logger.info(f"Comment {comment.id}: approved={comment.approved}, content={comment.content[:30]}")
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def pending_count(self, request):
        """Return the count of pending (unapproved) comments"""
        count = Comment.objects.filter(approved=False).count()
        logger.info(f"Pending comments count: {count}")
        return Response({'count': count}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get'])
    def debug(self, request):
        """Debug endpoint to check comments data and filter functionality"""
        # Get counts
        total_comments = Comment.objects.count()
        approved_comments = Comment.objects.filter(approved=True).count()
        pending_comments = Comment.objects.filter(approved=False).count()
        
        # Check if filtering works
        post_filter = request.query_params.get('post')
        approved_filter = request.query_params.get('approved')
        
        filtered_queryset = self.get_queryset()
        filtered_count = filtered_queryset.count()
        
        # Sample data
        sample_comments = []
        for comment in filtered_queryset[:5]:  # Get first 5 comments
            sample_comments.append({
                'id': comment.id,
                'post_id': comment.post_id,
                'content_preview': comment.content[:50] + ('...' if len(comment.content) > 50 else ''),
                'approved': comment.approved,
                'created_at': comment.created_at
            })
        
        # Return debug info
        debug_info = {
            'counts': {
                'total': total_comments,
                'approved': approved_comments,
                'pending': pending_comments,
                'filtered': filtered_count,
            },
            'filters_applied': {
                'post': post_filter,
                'approved': approved_filter,
            },
            'request_params': dict(request.query_params),
            'sample_comments': sample_comments
        }
        
        return Response(debug_info, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'patch'])
    def approve(self, request, pk=None):
        """Approve a comment"""
        comment = self.get_object()
        logger.info(f"Approving comment {comment.id} for post {comment.post.id}")
        logger.info(f"Comment status before: approved={comment.approved}")
        
        # Explicitly set approved to True
        comment.approved = True
        comment.save()
        
        # Verify the change was saved
        comment.refresh_from_db()
        logger.info(f"Comment status after: approved={comment.approved}")
        
        # Get all approved comments for this post for verification
        approved_count = Comment.objects.filter(post=comment.post, approved=True).count()
        logger.info(f"Post {comment.post.id} now has {approved_count} approved comments")
        
        # Return the updated comment data
        serializer = CommentSerializer(comment)
        return Response({
            'status': 'comment approved',
            'comment': serializer.data,
            'approved_count': approved_count
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'patch'])
    def reject(self, request, pk=None):
        """Reject (unapprove) a comment"""
        comment = self.get_object()
        logger.info(f"Rejecting comment {comment.id} for post {comment.post.id if comment.post else 'unknown'}")
        logger.info(f"Comment status before: approved={comment.approved}")
        
        # Set approved to False instead of deleting
        comment.approved = False
        comment.save()
        
        # Verify the change was saved
        comment.refresh_from_db()
        logger.info(f"Comment status after: approved={comment.approved}")
        
        # Return the updated comment data
        serializer = CommentSerializer(comment)
        return Response({
            'status': 'comment rejected',
            'comment': serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def bulk_approve(self, request):
        """Approve multiple comments at once"""
        comment_ids = request.data.get('comment_ids', [])
        if not comment_ids:
            return Response(
                {'error': 'No comment IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Log for debugging
        logger.info(f"Bulk approving comments: {comment_ids}")
        
        # Filter comments that aren't already approved
        comments = Comment.objects.filter(id__in=comment_ids, approved=False)
        count = comments.count()
        
        # Update the comments
        comments.update(approved=True, is_trash=False)
        
        logger.info(f"Bulk approved {count} comments")
        
        return Response({'status': f'{count} comments approved'}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['post'])
    def bulk_reject(self, request):
        """Reject (unapprove) multiple comments at once"""
        comment_ids = request.data.get('comment_ids', [])
        if not comment_ids:
            return Response(
                {'error': 'No comment IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Log for debugging
        logger.info(f"Bulk rejecting comments: {comment_ids}")
        
        # Filter comments that are currently approved
        comments = Comment.objects.filter(id__in=comment_ids, approved=True)
        count = comments.count()
        
        # Update comments to be unapproved (not deleted)
        comments.update(approved=False)
        
        logger.info(f"Bulk rejected {count} comments")
        
        return Response({'status': f'{count} comments rejected'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def all(self, request):
        """Return all comments (approved and pending) for a post"""
        post_id = request.query_params.get('post')
        if not post_id:
            return Response(
                {'error': 'Post ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        post = get_object_or_404(BlogPost, pk=post_id)
        approved_comments = Comment.objects.filter(post=post, approved=True)
        pending_comments = Comment.objects.filter(post=post, approved=False)
        
        return Response({
            'approved': CommentSerializer(approved_comments, many=True).data,
            'pending': CommentSerializer(pending_comments, many=True).data,
            'total': approved_comments.count() + pending_comments.count()
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def check_approved(self, request):
        """Check the status of approved comments for a specific post"""
        post_id = request.query_params.get('post')
        if not post_id:
            return Response(
                {'error': 'Post ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            post = BlogPost.objects.get(pk=post_id)
        except BlogPost.DoesNotExist:
            return Response(
                {'error': f'Post with ID {post_id} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get all comments for this post
        all_comments = Comment.objects.filter(post=post)
        
        # Count by approval status
        total_count = all_comments.count()
        approved_count = all_comments.filter(approved=True).count()
        unapproved_count = all_comments.filter(approved=False).count()
        
        # Get sample comments
        approved_samples = all_comments.filter(approved=True)[:5]
        unapproved_samples = all_comments.filter(approved=False)[:5]
        
        # Serialize sample comments
        approved_samples_data = CommentSerializer(approved_samples, many=True).data
        unapproved_samples_data = CommentSerializer(unapproved_samples, many=True).data
        
        return Response({
            'post_id': post_id,
            'post_title': post.title,
            'counts': {
                'total': total_count,
                'approved': approved_count,
                'unapproved': unapproved_count
            },
            'approved_samples': approved_samples_data,
            'unapproved_samples': unapproved_samples_data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def approved_for_post(self, request):
        """Get only approved comments for a specific post (dedicated endpoint)"""
        post_id = request.query_params.get('post')
        if not post_id:
            return Response(
                {'error': 'Post ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            post = BlogPost.objects.get(pk=post_id)
        except BlogPost.DoesNotExist:
            return Response(
                {'error': f'Post with ID {post_id} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Explicitly filter for approved comments only
        approved_comments = Comment.objects.filter(post=post, approved=True)
        
        # Log details for debugging
        logger.info(f"Getting approved comments for post {post_id}")
        logger.info(f"Found {approved_comments.count()} approved comments")
        
        # Return serialized data
        serializer = CommentSerializer(approved_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'patch', 'put', 'delete'])
    def reply(self, request, pk=None):
        """Add, update or delete an admin reply to a comment"""
        comment = self.get_object()
        
        # Handle DELETE request - remove admin reply
        if request.method == 'DELETE':
            comment.admin_reply = None
            comment.save()
            
            # Log for debugging
            logger.info(f"Deleted admin reply from comment {comment.id} for post {comment.post.id}")
            
            return Response({
                'status': 'reply deleted',
                'comment': CommentSerializer(comment).data
            }, status=status.HTTP_200_OK)
        
        # Handle POST, PATCH, PUT requests - add or update admin reply
        reply_text = request.data.get('admin_reply')
        
        if not reply_text:
            return Response(
                {'error': 'Reply content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        comment.admin_reply = reply_text
        comment.save()
        
        # Log for debugging
        logger.info(f"Added/updated admin reply to comment {comment.id} for post {comment.post.id}")
        
        # Return the updated comment data
        serializer = CommentSerializer(comment)
        return Response({
            'status': 'reply added' if request.method == 'POST' else 'reply updated',
            'comment': serializer.data
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_urls(request):
    """Debug view to list all URLs in the Django project."""
    urlconf = __import__(get_resolver().urlconf_name, fromlist=[''])
    
    def list_urls_recursive(patterns, parent_path=""):
        urls = []
        for pattern in patterns:
            if isinstance(pattern, URLPattern):
                # Get the pattern string or regex pattern
                pattern_str = str(pattern.pattern)
                # Append to parent path
                full_path = parent_path + pattern_str
                # Get the name if available
                name = pattern.name if hasattr(pattern, 'name') else ''
                # Get the callback function
                callback = pattern.callback.__name__ if hasattr(pattern.callback, '__name__') else str(pattern.callback)
                urls.append({
                    'path': full_path,
                    'name': name,
                    'callback': callback
                })
            elif isinstance(pattern, URLResolver):
                # Get resolver pattern
                resolver_path = str(pattern.pattern)
                # Recursively get patterns from resolver
                urls.extend(list_urls_recursive(pattern.url_patterns, parent_path + resolver_path))
        return urls
    
    try:
        all_urls = list_urls_recursive(urlconf.urlpatterns)
        # Filter for comment URLs to make output manageable
        comment_urls = [url for url in all_urls if 'comment' in url['path'].lower()]
        return JsonResponse({'comment_urls': comment_urls})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def comment_action(request, action):
    """Handle comment actions from admin interface"""
    try:
        comment_id = request.data.get('comment_id')
        if not comment_id:
            return JsonResponse({'error': 'Comment ID is required'}, status=400)
        
        # Log the request data for debugging
        logger.info(f"Comment action request: action={action}, comment_id={comment_id}, data={request.data}")
        
        comment = get_object_or_404(Comment, id=comment_id)
        
        if action == 'approve':
            comment.approved = True
            comment.is_trash = False
            comment.save()
            return JsonResponse({'status': 'success', 'message': 'Comment approved'})
            
        elif action == 'unapprove':
            comment.approved = False
            comment.save()
            return JsonResponse({'status': 'success', 'message': 'Comment unapproved'})
            
        elif action == 'trash':
            comment.is_trash = True
            comment.save()
            return JsonResponse({'status': 'success', 'message': 'Comment moved to trash'})
            
        elif action == 'restore':
            comment.is_trash = False
            comment.save()
            return JsonResponse({'status': 'success', 'message': 'Comment restored from trash'})
            
        elif action == 'delete':
            comment.delete()
            return JsonResponse({'status': 'success', 'message': 'Comment permanently deleted'})
            
        else:
            return JsonResponse({'error': f'Unknown action: {action}'}, status=400)
    
    except Exception as e:
        logger.error(f"Error performing comment action: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def comment_counts(request):
    """Get counts for comments in different states (all, pending, approved, trash)"""
    try:
        # Log the request for debugging
        logger.info(f"Received request to comment_counts endpoint: {request.path}")
        
        # Force evaluate the counts to ensure they're accurate
        all_count = Comment.objects.filter(is_trash=False).count()
        pending_count = Comment.objects.filter(approved=False, is_trash=False).count()
        approved_count = Comment.objects.filter(approved=True, is_trash=False).count()
        trash_count = Comment.objects.filter(is_trash=True).count()
        
        # Log counts for debugging
        logger.info(f"Comment counts: all={all_count}, pending={pending_count}, approved={approved_count}, trash={trash_count}")
        
        # Verify the counts match expectations
        total_count = Comment.objects.count()
        expected_sum = all_count + trash_count
        if total_count != expected_sum:
            logger.warning(f"Total comment count ({total_count}) doesn't match sum of all + trash ({expected_sum})")
        
        response_data = {
            'all': all_count,
            'pending': pending_count,
            'approved': approved_count,
            'trash': trash_count,
            'status': 'success',
            'message': 'Comment counts retrieved successfully',
            'path': request.path
        }
        
        # Return the response
        logger.info(f"Returning comment counts: {response_data}")
        return JsonResponse(response_data)
    except Exception as e:
        logger.error(f"Error getting comment counts: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e), 'detail': 'An error occurred while fetching comment counts'}, status=500)

@api_view(['GET'])
def test_api(request):
    """Simple test endpoint to verify API routing"""
    return JsonResponse({
        'status': 'success',
        'message': 'API test endpoint successful',
        'path': request.path,
        'method': request.method
    })
