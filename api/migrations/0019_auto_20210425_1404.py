# Generated by Django 3.2 on 2021-04-25 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0018_auto_20210425_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='medicines',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.medicine'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]