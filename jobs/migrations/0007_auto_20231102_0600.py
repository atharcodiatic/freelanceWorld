# Generated by Django 4.2.5 on 2023-11-02 06:00

from django.db import migrations

def add_value_to_remaining(apps, schema_editor):
    """
    The function used by the RunPython method to create a data migration, expects 
    two parameters: apps and schema_editor. The RunPython will feed those parameters.
    """
    Contract = apps.get_model('jobs', 'Contract')
    for cont in Contract.objects.all():
        cont.remaining = cont.total
        cont.save()
    

class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_contract_remaining'),
    ]

    operations = [
        migrations.RunPython(add_value_to_remaining),
    ]
