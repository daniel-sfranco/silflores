# Generated by Django 5.1.1 on 2025-02-18 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_cart_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Nome')),
                ('type', models.CharField(choices=[('fixed', 'fixo'), ('variable', 'porcentagem')], verbose_name='Tipo')),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
