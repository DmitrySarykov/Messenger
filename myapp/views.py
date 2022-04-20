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

class UserUpdateView(LoginRequiredMixin,UpdateView):
    model=UserProfile
    form_class = UserProfileForm
    template_name = 'account.html'
    
    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse_lazy('message_list')

class MessageListView(LoginRequiredMixin,ListView):
    model=Message
    template_name = 'message_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all() # Исключаем администраторов .exclude(is_superuser = True)
        context['group_list'] = Group.objects.all()
        return context

class ChatView(LoginRequiredMixin,ListView):
    model=Message
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

class GroupCreateView(LoginRequiredMixin,CreateView):
    model=Group
    form_class = GroupForm
    template_name = 'group_create.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['admin'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.save()
        group_pk = form.instance.pk
        group = Group.objects.get(pk = group_pk)
        users = form.cleaned_data['users']
        for user in users:
            obj = GroupUser.objects.create(group = group, user = user)
            obj.save()
        
        return super().form_valid(form)    
    
class GroupView(LoginRequiredMixin,TemplateView):
    model=Group
    template_name = 'group.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user_from'] = self.request.user.pk
        context['group'] = Group.objects.get(pk = self.kwargs['pk'])
        context['user_list'] = GroupUser.objects.filter(group = self.kwargs['pk'])
        context['message_list'] = Message.objects.filter(group = self.kwargs['pk'])
        return context  

# API
class MessageAPIView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageAPICreate(generics.CreateAPIView):
    serializer_class = MessageSerializer

class UserAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupListAPI(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupUpdateAPI(generics.CreateAPIView):
    serializer_class = GroupSerializer

class GroupUpdateAPI(generics.UpdateAPIView):
    serializer_class = GroupSerializer
    
    def get_object(self):
        obj = Group.objects.get(pk = self.kwargs['pk'])
        return obj
