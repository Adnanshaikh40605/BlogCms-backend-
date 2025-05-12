from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.BlogPostViewSet)
router.register(r'images', views.BlogImageViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('comments/pending-count/', views.CommentViewSet.as_view({'get': 'pending_count'}), name='comment-pending-count'),
    path('comments/all/', views.CommentViewSet.as_view({'get': 'all'}), name='comments-all'),
] 