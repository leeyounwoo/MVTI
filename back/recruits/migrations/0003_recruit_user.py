# Generated by Django 3.2.3 on 2021-11-25 03:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recruits', '0002_auto_20211123_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruit',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, related_name='otts', to=settings.AUTH_USER_MODEL),
        ),
    ]
