# Generated by Django 5.0.6 on 2024-08-08 11:46

import my_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourierShops',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shop_name', models.CharField(max_length=100)),
                ('owner_name', models.CharField(max_length=100)),
                ('phone_number', models.BigIntegerField(unique=True, validators=[my_app.models.validate_ten_digits])),
                ('mobile_number', models.BigIntegerField(unique=True, validators=[my_app.models.validate_ten_digits])),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('address', models.TextField()),
                ('city', models.TextField()),
                ('state', models.TextField()),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('billing_address', models.CharField(max_length=255)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
    ]
