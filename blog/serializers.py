from rest_framework import serializers
from .models import BlogPost, BlogImage, Comment

class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'approved', 'created_at', 'admin_reply']
        read_only_fields = ['id', 'approved', 'created_at']

class BlogPostListSerializer(serializers.ModelSerializer):
    featured_image = serializers.ImageField(max_length=None, use_url=True, required=False)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'featured_image', 'published', 'created_at']
        read_only_fields = ['id', 'created_at']

class BlogPostSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    featured_image = serializers.ImageField(max_length=None, use_url=True, required=False)
    additional_images = serializers.ListField(
        child=serializers.ImageField(max_length=None, allow_empty_file=False),
        write_only=True,
        required=False
    )
    
    def get_comments(self, obj):
        # Check if we have prefetched approved_comments
        if hasattr(obj, 'approved_comments'):
            return CommentSerializer(obj.approved_comments, many=True).data
        else:
            # Fallback to filtering (less efficient)
            comments = obj.comments.filter(approved=True)
            return CommentSerializer(comments, many=True).data
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'featured_image', 'images', 'comments', 
                 'additional_images', 'published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Extract additional images if present
        additional_images = []
        if 'additional_images' in validated_data:
            additional_images = validated_data.pop('additional_images', [])
        
        # Create the blog post
        blog_post = BlogPost.objects.create(**validated_data)
        
        # Create image entries for each additional image
        for image_data in additional_images:
            BlogImage.objects.create(post=blog_post, image=image_data)
            
        return blog_post
    
    def update(self, instance, validated_data):
        # Extract additional images if present
        additional_images = []
        if 'additional_images' in validated_data:
            additional_images = validated_data.pop('additional_images', [])
        
        # Update the blog post fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Create image entries for each additional image
        for image_data in additional_images:
            BlogImage.objects.create(post=instance, image=image_data)
            
        return instance 