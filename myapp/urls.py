from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("users/", UserListView.as_view(), name="user_list"),  
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("chat/<to_user>/", ChatView.as_view(), name="chat"),
    path("group/<pk>/", GroupView.as_view(), name="group"),
    path("group/create/", GroupCreateView.as_view(), name="group_create"),  
    path("account/<pk>/", UserUpdateView.as_view(), name="account_edit"),  
    
    # API
    path("api/user/list/", UserListAPI.as_view(), name="api_user_list"), 
    
    path("api/message/list/", MessageListAPI.as_view(), name="api_message_list"), 
    path("api/message/create/", MessageCreateAPI.as_view(), name="api_message_create"),
    
    path("api/group/list/", GroupListAPI.as_view(), name="api_group_list"),
    path("api/group/create/", GroupCreateAPI.as_view(), name="api_group_create"),
    path("api/group/update/<pk>", GroupUpdateAPI.as_view(), name="api_group_update"), 

 ]