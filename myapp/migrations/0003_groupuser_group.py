# Generated by Django 4.0.4 on 2022-04-19 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_message_user_message_from_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupuser',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.group', verbose_name='Группа'),
        ),
    ]
