from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path("<to_user>/chat/", ChatView.as_view(), name="chat"),
    path("group_create/", GroupCreateView.as_view(), name="group_create"),
    path("group/<pk>", GroupView.as_view(), name="group"),  
    path("<pk>/account/", UserUpdateView.as_view(), name="account_edit"),  
    # API
    path("api/user_list/", UserAPI.as_view(), name="api_user_list"), 
    path("api/message_list/", MessageAPIView.as_view(), name="api_message_list"), 
    path("api/message_create/", MessageAPICreate.as_view(), name="api_message_create"),
]