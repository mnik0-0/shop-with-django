# Generated by Django 3.0.7 on 2020-06-29 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20200629_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='Admin', max_length=30, verbose_name='name'),
            preserve_default=False,
        ),
    ]
