# Generated by Django 3.2.3 on 2021-11-24 03:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0002_comment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Review',
        ),
    ]
