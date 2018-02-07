from rest_framework import serializers

from postings.models import BlogPost


# Converts data to JSON and validate data passed
class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            'pk',
            'user',
            'title',
            'content',
            'timestamp'
        ]