# Generated by Django 4.2.2 on 2023-06-24 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_orders_phonenumber_alter_orders_zip_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=90)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('address1', models.CharField(max_length=120)),
                ('address2', models.CharField(max_length=120)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
    ]
