# Generated by Django 5.1 on 2024-09-04 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=250)),
                ('cat_image', models.ImageField(upload_to='images/category_image', verbose_name='cat_image')),
                ('no_of_products', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True, verbose_name='Available')),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/slider_image', verbose_name='slider_image')),
                ('is_active', models.BooleanField(default=True, verbose_name='Available')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=200)),
                ('sku', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default=0)),
                ('is_bestseller', models.BooleanField(default=True, verbose_name='BestSeller')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('description', models.TextField()),
                ('price', models.IntegerField(default=0)),
                ('is_customer_choice', models.BooleanField(default=True, verbose_name='CustomerChoice')),
                ('image1', models.ImageField(upload_to='images/products', verbose_name='product_image')),
                ('image2', models.ImageField(upload_to='images/products', verbose_name='product_image')),
                ('image3', models.ImageField(upload_to='images/products', verbose_name='product_image')),
                ('image4', models.ImageField(upload_to='images/products', verbose_name='product_image')),
                ('cat_id', models.ForeignKey(db_column='catid', default=0, on_delete=django.db.models.deletion.CASCADE, to='store_app.category')),
            ],
        ),
    ]
