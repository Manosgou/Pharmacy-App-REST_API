# Generated by Django 3.2 on 2021-04-25 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_pharmacistorder_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pharmacistorder',
            old_name='medicines',
            new_name='medicine',
        ),
    ]
