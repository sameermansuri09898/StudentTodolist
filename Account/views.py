from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Baseuser,Todolist
from .serializerreg import UserSerializer,LoginUser
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import generics
from .Todoserializer import TodolistSerializer
from rest_framework import viewsets
from django.contrib.auth import authenticate

class UserRegistrationView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class TodolistCreateView(viewsets.ViewSet):  
    permission_classes=[IsAuthenticated] 

    def list(self,request):
        queryset=Todolist.objects.filter(user=request.user)
        serializer=TodolistSerializer(queryset,many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer=TodolistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()   
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,pk=None):
        queryset=Todolist.objects.get(pk=pk)
        serializer=TodolistSerializer(queryset)
        return Response(serializer.data)

    def update(self,request,pk=None):
        queryset=Todolist.objects.get(pk=pk)
        serializer=TodolistSerializer(queryset,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        queryset=Todolist.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
      serilizer=LoginUser(data=request.data)
      if serilizer.is_valid():
        user=authenticate(request,username=serilizer.validated_data["username"],password=serilizer.validated_data["password"] )
        if user is not None:
          token,created=Token.objects.get_or_create(user=user)
          return Response({"token":token.key},status=status.HTTP_200_OK)
      return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)      
           