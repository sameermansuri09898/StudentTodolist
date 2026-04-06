from rest_framework import serializers
from .models import Baseuser

class UserSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True) 
    class Meta:
        model = Baseuser
        fields = ['username','email','password','confirm_password','Address','phone','image']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs    

    def get_image(self,obj):
        return obj.image.url if obj.image else None   

    def validate_email(self,value):
        if Baseuser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value  

    def validate_phone(self,value):
        if Baseuser.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone already exists")
        return value      

    def validate_username(self,value):
        if Baseuser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value  

    def create(self, validated_data):
          validated_data.pop('confirm_password')  

          password = validated_data.pop('password')

          user = Baseuser.objects.create_user(**validated_data)
          user.set_password(password) 
          user.save()

          return user