# Generated by Django 3.2 on 2021-04-27 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20210427_1339'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PharmacistOrder',
            new_name='Order',
        ),
    ]
