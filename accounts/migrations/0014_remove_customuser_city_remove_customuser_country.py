# Generated by Django 4.2.5 on 2023-11-08 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_skill_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='city',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='country',
        ),
    ]
