# Generated by Django 3.2 on 2021-04-25 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20210425_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='medicines',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.medicine'),
        ),
        migrations.DeleteModel(
            name='OrderMedicines',
        ),
    ]