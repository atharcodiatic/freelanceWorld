# Generated by Django 4.2.5 on 2023-10-11 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_skill_level_selfskills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freelancer',
            name='skills',
        ),
        migrations.RemoveField(
            model_name='selfskills',
            name='skill',
        ),
        migrations.AddField(
            model_name='selfskills',
            name='skill_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
