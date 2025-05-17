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
    list_display = ('author_info', 'content_preview', 'post_link', 'status_column', 'created_at')
    list_filter = ('approved', 'is_trash', 'created_at')
    search_fields = ('content', 'author_name', 'author_email', 'post__title')
    actions = ['approve_comments', 'unapprove_comments', 'trash_comments', 'restore_comments', 'delete_permanently']
    date_hierarchy = 'created_at'
    readonly_fields = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    
    class Media:
        js = ('js/admin/comment_actions.js',)
        
    fieldsets = (
        ('Author Information', {
            'fields': ('author_name', 'author_email', 'author_website', 'ip_address', 'user_agent'),
        }),
        ('Comment Content', {
            'fields': ('content', 'admin_reply'),
        }),
        ('Status', {
            'fields': ('approved', 'is_trash'),
        }),
        ('Related Post', {
            'fields': ('post',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def author_info(self, obj):
        if obj.author_name:
            author = obj.author_name
        else:
            author = "Anonymous"
            
        if obj.author_email:
            email = f"<br><a href='mailto:{obj.author_email}'>{obj.author_email}</a>"
        else:
            email = ""
            
        if obj.ip_address:
            ip = f"<br>{obj.ip_address}"
        else:
            ip = ""
            
        return format_html("{}{}{}", author, email, ip)
    author_info.short_description = 'Author'
    author_info.admin_order_field = 'author_name'
    
    def status_column(self, obj):
        if obj.is_trash:
            return format_html('<span style="color: red;">In Trash</span>')
        elif obj.approved:
            return format_html('<span style="color: green;">Approved</span>')
        else:
            return format_html('<span style="color: orange;">Pending</span>')
    status_column.short_description = 'Status'
    status_column.admin_order_field = 'approved'
    
    def post_link(self, obj):
        return format_html('<a href="{}">{}</a>', 
                          f'/admin/blog/blogpost/{obj.post.id}/change/', 
                          obj.post.title)
    post_link.short_description = 'Post'
    post_link.admin_order_field = 'post__title'
    
    def content_preview(self, obj):
        content = obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
        
        # Add row actions
        actions = []
        
        if obj.is_trash:
            actions.append(f'<a href="{obj.id}/change/">Edit</a>')
            actions.append(f'<a href="#" onclick="return approveComment({obj.id});">Restore</a>')
            actions.append(f'<a href="#" onclick="return deleteComment({obj.id});" style="color: red;">Delete Permanently</a>')
        else:
            actions.append(f'<a href="{obj.id}/change/">Edit</a>')
            
            if obj.approved:
                actions.append(f'<a href="#" onclick="return unapproveComment({obj.id});">Unapprove</a>')
            else:
                actions.append(f'<a href="#" onclick="return approveComment({obj.id});">Approve</a>')
                
            actions.append(f'<a href="#" onclick="return trashComment({obj.id});" style="color: red;">Trash</a>')
            
        action_html = ' | '.join(actions)
        
        return format_html('{}<br><div class="row-actions" style="margin-top: 6px; color: #999;">{}</div>',
                          content, action_html)
    content_preview.short_description = 'Comment'
    content_preview.admin_order_field = 'content'

    def approve_comments(self, request, queryset):
        updated = queryset.update(approved=True, is_trash=False)
        self.message_user(request, f'{updated} comment(s) have been approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f'{updated} comment(s) have been unapproved.')
    unapprove_comments.short_description = "Unapprove selected comments"
    
    def trash_comments(self, request, queryset):
        updated = queryset.update(is_trash=True)
        self.message_user(request, f'{updated} comment(s) have been moved to trash.')
    trash_comments.short_description = "Move selected comments to trash"
    
    def restore_comments(self, request, queryset):
        updated = queryset.update(is_trash=False)
        self.message_user(request, f'{updated} comment(s) have been restored from trash.')
    restore_comments.short_description = "Restore selected comments from trash"
    
    def delete_permanently(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} comment(s) have been permanently deleted.')
    delete_permanently.short_description = "Delete selected comments permanently"
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related('post')
        
        # Apply filters based on URL parameters
        is_trash = request.GET.get('is_trash')
        if is_trash == '1':
            return queryset.filter(is_trash=True)
        else:
            queryset = queryset.filter(is_trash=False)
            
        approved = request.GET.get('approved')
        if approved == '1':
            return queryset.filter(approved=True)
        elif approved == '0':
            return queryset.filter(approved=False)
            
        return queryset
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.GET.get('is_trash', '0') == '1':
            # If viewing trash, show restore and delete permanently options, but hide approve/unapprove/trash
            if 'approve_comments' in actions:
                del actions['approve_comments']
            if 'unapprove_comments' in actions:
                del actions['unapprove_comments']
            if 'trash_comments' in actions:
                del actions['trash_comments']
        else:
            # If not viewing trash, hide restore and delete permanently options
            if 'restore_comments' in actions:
                del actions['restore_comments']
            if 'delete_permanently' in actions:
                del actions['delete_permanently']
        return actions

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
