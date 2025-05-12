from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from .models import BlogPost, BlogImage, Comment
from .serializers import (
    BlogPostSerializer, 
    BlogPostListSerializer, 
    BlogImageSerializer, 
    CommentSerializer
)

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
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def pending_count(self, request):
        """Return the count of pending (unapproved) comments"""
        count = Comment.objects.filter(approved=False).count()
        return Response({'count': count}, status=status.HTTP_200_OK)
    
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
            
        # Get all comments for the post
        comments = Comment.objects.filter(post=post_id).order_by('-created_at')
        
        # Split them into approved and pending
        approved = comments.filter(approved=True)
        pending = comments.filter(approved=False)
        
        # Serialize both
        approved_data = CommentSerializer(approved, many=True).data
        pending_data = CommentSerializer(pending, many=True).data
        
        return Response({
            'approved': approved_data,
            'pending': pending_data,
            'total': len(approved_data) + len(pending_data)
        }, status=status.HTTP_200_OK)
