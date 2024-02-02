from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'technology', 'created_at', 'user') 
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super(ProjectSerializer, self).create(validated_data)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    

    