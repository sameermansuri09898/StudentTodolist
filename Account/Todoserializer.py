from .models import Todolist
from rest_framework import serializers

class TodolistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields = ['id','title','description','created_at','updated_at','user']
        extra_kwargs = {
            'user': {'read_only': True}
        }
    def validate(self, attrs):
        if attrs['title'] == attrs['description']:
            raise serializers.ValidationError("Title and description cannot be same")
        return attrs    
        
    def create(self, validated_data):
        return Todolist.objects.create(**validated_data)    
    