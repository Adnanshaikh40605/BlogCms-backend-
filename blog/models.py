from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Content', config_name='extends')
    featured_image = models.ImageField(upload_to='featured_images/', blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    published = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Optimize featured image if present
        if self.featured_image:
            try:
                # Open image using PIL
                img = Image.open(self.featured_image)
                
                # Prepare BytesIO object
                img_io = BytesIO()
                
                # Try to convert to WebP if RGB/RGBA
                if img.mode in ('RGB', 'RGBA'):
                    # Save as WebP format
                    img.save(img_io, format='WEBP', quality=85, optimize=True)
                    
                    # Get original filename and change extension
                    filename = os.path.splitext(os.path.basename(self.featured_image.name))[0]
                    new_filename = f"{filename}.webp"
                    
                    # Save the optimized image
                    self.featured_image.save(
                        new_filename,
                        ContentFile(img_io.getvalue()),
                        save=False  # Don't trigger recursive save
                    )
                    logger.info(f"Converted featured image to WebP: {new_filename}")
                else:
                    # Just compress in original format
                    img_format = img.format if img.format else 'JPEG'
                    img.save(img_io, format=img_format, quality=85, optimize=True)
                    self.featured_image.save(
                        self.featured_image.name,
                        ContentFile(img_io.getvalue()),
                        save=False
                    )
                    logger.info(f"Compressed featured image: {self.featured_image.name}")
            except Exception as e:
                logger.error(f"Error optimizing featured image: {str(e)}")
        
        super().save(*args, **kwargs)

class BlogImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.post.title}"

    def save(self, *args, **kwargs):
        """Optimize image on save"""
        if self.image:
            self.optimize_image()
        super().save(*args, **kwargs)
    
    def optimize_image(self, quality=85, convert_to_webp=True):
        """Compress image and optionally convert to WebP format"""
        try:
            # Open image using PIL
            img = Image.open(self.image)
            
            # If convert to WebP is requested and format is supported
            if convert_to_webp and img.mode in ('RGB', 'RGBA'):
                # Prepare BytesIO object to save the image
                img_io = BytesIO()
                
                # Save as WebP format with specified quality
                img.save(img_io, format='WEBP', quality=quality, optimize=True)
                
                # Get original filename and change extension
                filename = os.path.splitext(os.path.basename(self.image.name))[0]
                new_filename = f"{filename}.webp"
                
                # Save the optimized image back to the model field
                self.image.save(
                    new_filename,
                    ContentFile(img_io.getvalue()),
                    save=False  # Don't trigger recursive save
                )
                logger.info(f"Converted image to WebP: {new_filename}")
            else:
                # If WebP not requested or not supported, just compress in original format
                img_io = BytesIO()
                img_format = img.format if img.format else 'JPEG'
                
                # Save with quality settings
                img.save(img_io, format=img_format, quality=quality, optimize=True)
                
                # Save the optimized image back to the model field
                self.image.save(
                    self.image.name,
                    ContentFile(img_io.getvalue()),
                    save=False  # Don't trigger recursive save
                )
                logger.info(f"Compressed image: {self.image.name}")
                
        except Exception as e:
            logger.error(f"Error optimizing image: {str(e)}")

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments', db_index=True)
    author_name = models.CharField(max_length=100, blank=True, null=True)
    author_email = models.EmailField(blank=True, null=True)
    author_website = models.URLField(blank=True, null=True)
    content = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False, db_index=True)
    is_trash = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_reply = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'approved']),
            models.Index(fields=['is_trash']),
        ] 