# Generated by Django 5.1.1 on 2024-09-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('size_type', models.CharField(choices=[('fixed', 'Tamanho fixo'), ('choice', 'Selecionar tamanho'), ('set', 'Definir valor')])),
                ('size', models.CharField()),
                ('term', models.IntegerField()),
                ('tags', models.ManyToManyField(to='products.tag')),
            ],
        ),
    ]