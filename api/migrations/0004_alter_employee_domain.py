# Generated by Django 3.2 on 2021-04-15 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='domain',
            field=models.CharField(choices=[('PH', 'Pharmacist'), ('SP', 'Supplier')], default='PH', max_length=2),
        ),
    ]
