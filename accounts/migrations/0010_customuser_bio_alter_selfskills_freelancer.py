# Generated by Django 4.2.5 on 2023-10-18 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_freelancer_skills_remove_selfskills_skill_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='selfskills',
            name='freelancer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.freelancer'),
        ),
    ]
