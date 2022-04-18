from django.contrib import admin
from django.urls import path, include
from .views import MessageAPIView
urlpatterns = [
    path("api/message_list/", MessageAPIView.as_view(), name="message_list"),
    
]