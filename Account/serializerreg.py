
from rest_framework import serializers
from .models import Baseuser,Todolist

class UserSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True) 
    class Meta:
        model = Baseuser
        fields = ['username','email','password','confirm_password','address','phone','image']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs    

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
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
         validated_data.pop('confirm_password', None)
         password = validated_data.pop('password')

         user = Baseuser(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            address=validated_data.get('address'),
            image=validated_data.get('image'),  
         )
         user.set_password(password)   # ✅ correct hashing
         user.save()

         return user


class TodolistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields = ['id','title','description','created_at','updated_at','user']
        extra_kwargs = {
            'user': {'read_only': True}
        }    
    def create(self, validated_data):
        return Todolist.objects.create(**validated_data)    

class LoginUser(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    class Meta:
        model=Baseuser
        fields=['username','password']