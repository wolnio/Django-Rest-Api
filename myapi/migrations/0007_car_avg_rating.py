# Generated by Django 3.2.9 on 2021-11-23 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0006_auto_20211123_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
    ]