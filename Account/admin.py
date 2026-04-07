
from django.contrib import admin
from .models import Baseuser,Todolist
# Register your models here.
admin.site.register(Baseuser)
admin.site.register(Todolist)

class TodolistAdmin(admin.ModelAdmin):
    list_display = ('title','description','created_at','updated_at','user')
    list_filter = ('created_at','updated_at')
    search_fields = ('title','description')
    ordering = ('-created_at',) 

class BaseuserAdmin(admin.ModelAdmin):
    list_display = ('username','email','phone','address','image')
    list_filter = ('username','email','phone','address','image')
    search_fields = ('username','email','phone','address','image')
    ordering = ('-username',) 