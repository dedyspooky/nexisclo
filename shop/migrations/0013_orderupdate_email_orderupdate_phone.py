# Generated by Django 4.2.2 on 2023-06-25 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_orderupdate_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderupdate',
            name='email',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='orderupdate',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
    ]
