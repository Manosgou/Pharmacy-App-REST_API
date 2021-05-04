# Generated by Django 3.2 on 2021-04-25 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20210425_1326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='medicines',
        ),
        migrations.CreateModel(
            name='OrderMedicines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.medicine')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='medicines',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ordermedicines'),
        ),
    ]