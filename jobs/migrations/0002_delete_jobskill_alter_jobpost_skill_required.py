# Generated by Django 4.2.5 on 2023-10-20 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_customuser_gender_alter_customuser_profile_pic_and_more'),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='JobSkill',
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='skill_required',
            field=models.ManyToManyField(to='accounts.skill'),
        ),
    ]