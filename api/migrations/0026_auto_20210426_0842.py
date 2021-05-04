# Generated by Django 3.2 on 2021-04-26 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_pharmacistorder_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pharmacistorder',
            name='user',
        ),
        migrations.AddField(
            model_name='pharmacistorder',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.employee'),
        ),
    ]
