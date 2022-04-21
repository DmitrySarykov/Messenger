from django.db import models
from datetime import date, datetime
from django.utils import dateformat
from django.contrib.auth.models import User
from django.urls import reverse

# Профиль
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/images/users/', verbose_name='Аватарка',null=True, blank=True)

    def __str__(self):
        return f'{self.user}'
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

# Группа
class Group(models.Model):
    admin = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Создатель группы', related_name="user_admin",null=True)
    name = models.CharField(max_length=200, verbose_name='Название группы',)
    users = models.ManyToManyField(User, blank=True, verbose_name='Участники')
    avatar = models.ImageField(upload_to='static/images/groups/', verbose_name='Аватарка',null=True, blank=True) 

    def get_absolute_url(self):
        return reverse('group', kwargs={'pk' : self.pk})   

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

# Сообщение 
class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='От кого', related_name="from_user",null=True,)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кому',null=True, blank=True, related_name="to_user")
    group = models.ForeignKey(Group,on_delete=models.CASCADE, verbose_name='Группа', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    message = models.TextField(verbose_name='Сообщение', null=True)

    def __str__(self):
        return f'{dateformat.format(self.date, "d.m.Y H:i:s")} {self.from_user}: {self.message}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
