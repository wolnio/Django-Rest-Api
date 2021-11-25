# Generated by Django 3.2.9 on 2021-11-23 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0004_remove_car_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrate',
            name='car',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='myapi.car'),
        ),
        migrations.AlterField(
            model_name='carrate',
            name='rate',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
