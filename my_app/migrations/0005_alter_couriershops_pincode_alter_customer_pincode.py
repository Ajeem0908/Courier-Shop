# Generated by Django 5.0.7 on 2024-08-12 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_alter_delivery_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couriershops',
            name='pincode',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='customer',
            name='pincode',
            field=models.CharField(max_length=10),
        ),
    ]
