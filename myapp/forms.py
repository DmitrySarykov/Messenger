from django import forms
from .models import *

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
