# Generated by Django 4.2.5 on 2023-10-11 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_freelancer_skills_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='level',
        ),
        migrations.CreateModel(
            name='SelfSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('BEG', 'BEGINEER'), ('INT', 'INTERMIDIATE'), ('EXP', 'EXPERT')], max_length=3)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.freelancer')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.skill')),
            ],
        ),
    ]