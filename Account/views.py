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
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        print("ERROR 👉", serializer.errors)   # 👈 ADD THIS
        return Response(serializer.errors, status=400)

class TodolistCreateView(viewsets.ViewSet):

    authentication_classes = [TokenAuthentication]   # ✅ ADD THIS
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Todolist.objects.filter(user=request.user)
        serializer = TodolistSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TodolistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)   # ✅ FIX THIS ALSO
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        queryset = Todolist.objects.get(user=request.user, pk=pk)
        serializer = TodolistSerializer(queryset, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Todolist.objects.get(user=request.user,pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = LoginUser(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"]
            )

            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=200)

            return Response({"error": "Invalid credentials"}, status=401)

        return Response(serializer.errors, status=400)
           



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the user's token
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)           