# Generated by Django 3.2 on 2021-04-25 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20210425_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='medicines',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.medicine'),
        ),
    ]