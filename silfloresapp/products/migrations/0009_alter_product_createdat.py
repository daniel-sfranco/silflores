# Generated by Django 5.1.1 on 2025-04-22 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_createdat_product_updatedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
