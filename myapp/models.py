from email import message
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Сообщения 
class Message(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateTimeField(default=datetime.now, verbose_name='Дата')
    message = models.TextField(verbose_name='Сообщение', null=True)

    def __str__(self):
        return f'{self.user} {self.date} {self.message}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'