# Generated by Django 5.1.1 on 2025-01-20 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.CharField(default='open'),
        ),
    ]
