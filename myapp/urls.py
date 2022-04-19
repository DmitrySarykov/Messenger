from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # API
    path("api/message_list/", MessageAPIView.as_view(), name="api_message_list"),
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path("<to_user>/chat/", ChatView.as_view(), name="chat"),
    path("group_create/", GroupCreateView.as_view(), name="group_create"),
    path("group/<pk>", GroupView.as_view(), name="group"),      
]