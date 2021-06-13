# Generated by Django 3.2 on 2021-06-01 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0037_auto_20210531_2300'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employee',
            new_name='UserProfile',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='employee',
            new_name='user_profile',
        ),
        migrations.RemoveField(
            model_name='location',
            name='employee',
        ),
        migrations.AddField(
            model_name='location',
            name='user_profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.userprofile'),
        ),
    ]