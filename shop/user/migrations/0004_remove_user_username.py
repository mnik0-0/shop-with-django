# Generated by Django 3.0.7 on 2020-06-26 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
