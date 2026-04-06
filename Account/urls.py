from django.urls import path,include
from .views import UserRegistrationView
from rest_framework.routers import DefaultRouter
from .views import TodolistCreateView,LoginView

router=DefaultRouter()
router.register(r"todolist",TodolistCreateView,basename="todolist")

urlpatterns = [
    path("register/",UserRegistrationView.as_view(),name="register"),
    path("login/",LoginView.as_view(),name="login"),  
    path("",include(router.urls)),
]
