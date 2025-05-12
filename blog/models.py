from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    featured_image = models.ImageField(upload_to='featured_images/', blank=True, null=True)
    published = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class BlogImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments', db_index=True)
    content = models.TextField()
    approved = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Comment on {self.post.title}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'approved']),
        ] 