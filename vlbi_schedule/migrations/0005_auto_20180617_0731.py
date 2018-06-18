# Generated by Django 2.0.5 on 2018-06-17 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vlbi_schedule', '0004_auto_20180615_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='band',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='observation',
            name='description',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='observation',
            name='observation_ID',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
