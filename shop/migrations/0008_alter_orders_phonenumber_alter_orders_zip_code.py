# Generated by Django 4.2.2 on 2023-06-24 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_orders_alter_contact_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='phonenumber',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orders',
            name='zip_code',
            field=models.IntegerField(),
        ),
    ]
