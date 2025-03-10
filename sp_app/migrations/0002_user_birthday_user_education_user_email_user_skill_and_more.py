# Generated by Django 5.1.5 on 2025-02-02 15:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sp_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='education',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='user',
            name='skill',
            field=models.TextField(default='什麼都不會'),
        ),
        migrations.AlterField(
            model_name='user',
            name='account',
            field=models.TextField(max_length=12),
        ),
        migrations.AlterField(
            model_name='user',
            name='desription',
            field=models.TextField(default='這個人很懶，還沒留下任何東西~'),
        ),
        migrations.AlterField(
            model_name='user',
            name='headshot',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.TextField(default=''),
        ),
    ]
