from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.BlogPostViewSet)
router.register(r'images', views.BlogImageViewSet)
router.register(r'comments', views.CommentViewSet)

# These explicit paths override the default router paths for special actions
urlpatterns = [
    # Include router-generated URLs
    path('', include(router.urls)),
    
    # Test endpoints for API routing
    path('test/', views.test_api, name='api-test'),
    
    # Special comment endpoints (keep consistent naming with frontend)
    path('comments/pending-count/', views.CommentViewSet.as_view({'get': 'pending_count'}), name='comment-pending-count'),
    path('comments/all/', views.CommentViewSet.as_view({'get': 'all'}), name='comments-all'),
    path('comments/debug/', views.CommentViewSet.as_view({'get': 'debug'}), name='comments-debug'),
    path('comments/check-approved/', views.CommentViewSet.as_view({'get': 'check_approved'}), name='comments-check-approved'),
    path('comments/approved-for-post/', views.CommentViewSet.as_view({'get': 'approved_for_post'}), name='comments-approved-for-post'),
    
    # Also provide underscore versions for better API compatibility
    path('comments/pending_count/', views.CommentViewSet.as_view({'get': 'pending_count'}), name='comment-pending-count-alt'),
    
    # Bulk operations
    path('comments/bulk_approve/', views.CommentViewSet.as_view({'post': 'bulk_approve'}), name='comments-bulk-approve'),
    path('comments/bulk_reject/', views.CommentViewSet.as_view({'post': 'bulk_reject'}), name='comments-bulk-reject'),
    
    # Comment admin action endpoints
    path('comments/approve/', views.comment_action, {'action': 'approve'}, name='comment-approve'),
    path('comments/unapprove/', views.comment_action, {'action': 'unapprove'}, name='comment-unapprove'),
    path('comments/trash/', views.comment_action, {'action': 'trash'}, name='comment-trash'),
    path('comments/restore/', views.comment_action, {'action': 'restore'}, name='comment-restore'),
    path('comments/delete/', views.comment_action, {'action': 'delete'}, name='comment-delete'),
    
    # Debug URL for troubleshooting
    path('debug/urls/', views.list_urls, name='debug-list-urls'),
    
    # Comment counts endpoint - direct path
    path('comments/counts/', views.comment_counts, name='comment-counts'),
    
    # Add a direct pattern matcher to ensure the full path works
    re_path(r'^comments/counts/?$', views.comment_counts, name='comment-counts-regex'),
] 