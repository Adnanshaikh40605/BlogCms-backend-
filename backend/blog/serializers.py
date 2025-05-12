from rest_framework import serializers
from .models import BlogPost, FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'order']

class BlogPostSerializer(serializers.ModelSerializer):
    faqs = FAQSerializer(many=True, required=False)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'featured_image',
            'category', 'created_at', 'updated_at', 'published',
            'faqs', 'read_time'
        ]

    def create(self, validated_data):
        faqs_data = validated_data.pop('faqs', [])
        post = BlogPost.objects.create(**validated_data)
        
        for faq_data in faqs_data:
            faq = FAQ.objects.create(**faq_data)
            post.faqs.add(faq)
        
        return post

    def update(self, instance, validated_data):
        faqs_data = validated_data.pop('faqs', [])
        
        # Update the blog post fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Clear existing FAQs and create new ones
        instance.faqs.clear()
        for faq_data in faqs_data:
            faq = FAQ.objects.create(**faq_data)
            instance.faqs.add(faq)
        
        return instance 