from django.urls import path, include
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
] 