# Generated by Django 3.2 on 2021-04-24 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_employee_pharmancy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='pharmancy',
        ),
        migrations.AddField(
            model_name='pharmancy',
            name='employee',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.employee'),
        ),
    ]
