# Generated by Django 4.2.5 on 2023-11-15 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_customuser_city_customuser_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='pin_code',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=10),
        ),
    ]