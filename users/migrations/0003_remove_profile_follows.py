# Generated by Django 2.2.7 on 2019-12-06 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='follows',
        ),
    ]