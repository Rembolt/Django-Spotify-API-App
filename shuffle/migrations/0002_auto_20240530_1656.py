# Generated by Django 3.1.6 on 2024-05-30 20:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shuffle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='accessToken',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='tokenMaxTime',
            field=models.IntegerField(default=6400),
        ),
        migrations.AddField(
            model_name='user',
            name='tokenRequestTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
