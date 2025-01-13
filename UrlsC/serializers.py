from rest_framework import serializers
from .models import Urls
from django.contrib.auth.models import User

class UrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urls
        fields = ['id', 'original_url', 'shortened_url', 'is_private', 'view_count', 'created_by', 'created_at']
        read_only_fields = ['shortened_url', 'view_count', 'created_by', 'created_at']
