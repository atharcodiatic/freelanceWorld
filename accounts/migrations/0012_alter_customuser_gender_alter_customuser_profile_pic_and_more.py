# Generated by Django 4.2.5 on 2023-10-19 10:45

import accounts.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_client_options_alter_freelancer_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/', validators=[accounts.validators.validate_image, django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg'], message='only jpeg and png extensions allowed')]),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'txt', 'doc'], message='only pdf , txt , doc extensions allowed')]),
        ),
    ]
