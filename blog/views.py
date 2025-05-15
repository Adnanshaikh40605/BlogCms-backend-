from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
import logging

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
            elif approved.lower() == 'false':
                queryset = queryset.filter(approved=False)
                
        # Log the query for debugging
        logger.debug(f"Comment queryset filters: post={post}, approved={approved}")
        logger.debug(f"Comment queryset count: {queryset.count()}")
        
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
        comment.approved = True
        comment.save()
        return Response({'status': 'comment approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'patch'])
    def reject(self, request, pk=None):
        """Reject a comment by deleting it"""
        comment = self.get_object()
        comment.delete()
        return Response({'status': 'comment rejected and deleted'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def bulk_approve(self, request):
        """Approve multiple comments at once"""
        comment_ids = request.data.get('comment_ids', [])
        if not comment_ids:
            return Response(
                {'error': 'No comment IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        comments = Comment.objects.filter(id__in=comment_ids, approved=False)
        count = comments.count()
        comments.update(approved=True)
        
        return Response({'status': f'{count} comments approved'}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['post'])
    def bulk_reject(self, request):
        """Reject (delete) multiple comments at once"""
        comment_ids = request.data.get('comment_ids', [])
        if not comment_ids:
            return Response(
                {'error': 'No comment IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        comments = Comment.objects.filter(id__in=comment_ids)
        count = comments.count()
        comments.delete()
        
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
