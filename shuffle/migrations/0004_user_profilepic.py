# Generated by Django 3.1.6 on 2024-05-31 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuffle', '0003_auto_20240530_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profilePic',
            field=models.TextField(blank=True),
        ),
    ]
