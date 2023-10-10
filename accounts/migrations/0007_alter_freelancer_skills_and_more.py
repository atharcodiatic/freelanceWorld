# Generated by Django 4.2.5 on 2023-10-09 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_education_skill_alter_client_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='skills',
            field=models.ManyToManyField(blank=True, to='accounts.skill'),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='years_of_experience',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
