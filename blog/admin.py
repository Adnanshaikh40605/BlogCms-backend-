from django.contrib import admin
from .models import BlogPost, BlogImage, Comment
from django.utils.html import format_html

class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['content', 'created_at']
    classes = ['collapse']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content')
    inlines = [BlogImageInline, CommentInline]
    save_on_top = True
    list_per_page = 20
    date_hierarchy = 'created_at'
    actions_on_top = True
    actions_on_bottom = True
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'content'),
            'classes': ('wide',),
        }),
        ('Publication', {
            'fields': ('published', 'featured_image'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def view_on_site(self, obj):
        return f"/api/posts/{obj.id}/"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'content_preview', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('content', 'post__title')
    actions = ['approve_comments', 'reject_comments']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Comment'

    def approve_comments(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f'{updated} comment(s) have been approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def reject_comments(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f'{updated} comment(s) have been rejected.')
    reject_comments.short_description = "Reject selected comments"

@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__title',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'
