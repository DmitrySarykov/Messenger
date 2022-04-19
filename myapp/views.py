from msilib.schema import ListView
from wsgiref.simple_server import server_version
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rest_framework import generics
from .models import *
from .forms import *
from .serializers import MessageSerializer
from django.contrib.auth.models import User
from django.db.models import Q


class HomeView(TemplateView):
    template_name = 'myapp/message_list.html'
    def get(self, *args, **kwargs):
        return redirect('message_list')

class MessageListView(ListView):
    model=Message
    template_name = 'message_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all().exclude(is_superuser = True) # Исключаем администраторов
        context['group_list'] = Group.objects.all()
        return context

class ChatView(CreateView):
    model=Message
    form_class = MessageForm
    template_name = 'chat.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['to_user'] = self.kwargs['to_user']
        initial['from_user'] = self.request.user
        return initial

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user_from'] = self.request.user
        context['user_to'] = User.objects.get(pk = self.kwargs['to_user'])
        context['message_list'] = Message.objects.filter(
            Q(from_user = self.kwargs['to_user']) & Q(to_user = self.request.user) |
            Q(from_user = self.request.user) & Q(to_user = self.kwargs['to_user'])
        ).order_by("date")
        return context
    
    def get_success_url(self):
        to_user=self.kwargs['to_user']
        return reverse_lazy('chat', kwargs={'to_user': to_user})

class GroupCreateView(CreateView):
    model=Group
    form_class = GroupForm
    template_name = 'group_create.html'    
    
class GroupView(TemplateView):
    model=Group
    template_name = 'group.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.get(pk = self.kwargs['pk'])
        context['user_list'] = GroupUser.objects.filter(group = self.kwargs['pk'])
        context['message_list'] = Message.objects.filter(group = self.kwargs['pk'])
        return context  

# API
class MessageAPIView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer