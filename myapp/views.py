from tokenize import group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from requests import Response
from rest_framework import generics
from .models import *
from .forms import *
from .serializers import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'myapp/message_list.html'
    def get(self, *args, **kwargs):
        return redirect('message_list')

class UserListView(LoginRequiredMixin,ListView):
    model = User
    template_name = 'user_list.html'
    
class UserUpdateView(LoginRequiredMixin,TemplateView):
    model = UserProfile
    template_name = 'account.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context 

class MessageListView(LoginRequiredMixin,ListView):
    model = Message
    template_name = 'message_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user_list = []
        for user in User.objects.all():
            if len( Message.objects.filter(
            Q(from_user = user) & Q(to_user = self.request.user) |
            Q(from_user = self.request.user) & Q(to_user = user)) ) > 0:
                user_list.append(user)    
        context['user_list'] = user_list
        
        group_list = []
        for group in Group.objects.all():
            if self.request.user.pk in list(group.users.values_list("pk", flat=True)) or self.request.user == group.admin:
                group_list.append(group)
        context['group_list'] = group_list
        
        return context

class ChatView(LoginRequiredMixin,ListView):
    model = Message
    template_name = 'chat.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user_from'] = self.request.user
        context['user_to'] = User.objects.get(pk = self.kwargs['to_user'])
        context['message_list'] = Message.objects.filter(
            Q(from_user = self.kwargs['to_user']) & Q(to_user = self.request.user) |
            Q(from_user = self.request.user) & Q(to_user = self.kwargs['to_user'])
        ).order_by("date")
        return context

class GroupCreateView(LoginRequiredMixin,TemplateView):
    template_name = 'group_create.html'  
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user_admin'] = self.request.user
        context['user_list'] = User.objects.all()
        return context  

class GroupView(LoginRequiredMixin,TemplateView):
    template_name = 'group.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user_from'] = self.request.user.pk
        context['group'] = Group.objects.get(pk = self.kwargs['pk'])
        context['message_list'] = Message.objects.filter(group = self.kwargs['pk'])
        return context  

# API Message
class MessageListAPI(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageCreateAPI(generics.CreateAPIView):
    serializer_class = MessageSerializer

# API User
class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAPI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateAPI(generics.UpdateAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        obj = User.objects.get(pk = self.kwargs['pk'])
        return obj

class AvatarUpdateAPI(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        obj = UserProfile.objects.get(pk = self.kwargs['pk'])
        return obj

# API Chat
class ChatAPI(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        queryset = Message.objects.filter(
            Q(from_user = self.request.user.pk) & Q(to_user = self.kwargs["pk"]) |
            Q(from_user = self.kwargs["pk"]) & Q(to_user = self.request.user.pk))
        return queryset

# API Group
class GroupListAPI(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupAPI(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        queryset = Message.objects.filter(group = self.kwargs['pk'])
        return queryset

class GroupCreateAPI(generics.CreateAPIView):
    serializer_class = GroupSerializer

class GroupUpdateAPI(generics.UpdateAPIView):
    serializer_class = GroupSerializer
    
    def get_object(self):
        obj = Group.objects.get(pk = self.kwargs['pk'])
        return obj

class GroupDeleteAPI(generics.DestroyAPIView):
    serializer_class = GroupSerializer
    
    def get_object(self):
        obj = Group.objects.get(pk = self.kwargs['pk'])
        return obj




