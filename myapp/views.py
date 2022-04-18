from wsgiref.simple_server import server_version
from django.shortcuts import render
from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer

class MessageAPIView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    
