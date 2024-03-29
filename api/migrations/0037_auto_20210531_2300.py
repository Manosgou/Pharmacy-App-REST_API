# Generated by Django 3.2 on 2021-05-31 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0036_auto_20210522_1321'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='Employee',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.employee'),
        ),
    ]
