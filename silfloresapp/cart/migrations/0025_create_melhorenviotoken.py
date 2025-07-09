from django.db import migrations


def create_melhorenviotoken(apps, schema_editor):
    Token = apps.get_model('cart', 'MelhorEnvioToken')
    Token.objects.create(expires_in=0)


class Migration(migrations.Migration):
    dependencies = [
        ('cart', '0024_alter_cart_freightoption'),
    ]

    operations = [
        migrations.RunPython(create_melhorenviotoken)
    ]
