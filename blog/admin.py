from django.contrib import admin
from .models import BlogPost, BlogImage, Comment

class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['content', 'created_at']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content')
    inlines = [BlogImageInline, CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('content',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f'{updated} comment(s) have been approved.')
    approve_comments.short_description = "Approve selected comments"
