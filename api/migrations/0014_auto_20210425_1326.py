# Generated by Django 3.2 on 2021-04-25 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='medicines',
        ),
        migrations.AddField(
            model_name='order',
            name='medicines',
            field=models.ManyToManyField(to='api.Medicine'),
        ),
    ]