# Generated by Django 5.1.1 on 2024-10-17 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_numphotos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.FileField(blank=True, upload_to='products/'),
        ),
    ]