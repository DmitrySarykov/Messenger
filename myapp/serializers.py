from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("from_user","to_user","date","message")