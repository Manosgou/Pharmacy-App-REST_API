# Generated by Django 3.2 on 2021-04-24 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_pharmancy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pharmancy',
            name='employee',
        ),
        migrations.AddField(
            model_name='employee',
            name='pharmancy',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.pharmancy'),
        ),
    ]
