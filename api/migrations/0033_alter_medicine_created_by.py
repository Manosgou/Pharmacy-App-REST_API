# Generated by Django 3.2 on 2021-05-06 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_alter_location_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='created_by',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.employee'),
        ),
    ]