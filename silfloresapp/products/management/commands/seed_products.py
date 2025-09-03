import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product, Tag

class Command(BaseCommand):
    help = 'Deletes all products and seeds the database with a fresh set of sample products.'

    def handle(self, *args, **options):
        self.stdout.write('Deleting all existing products...')
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All products deleted.'))

        self.stdout.write('Re-seeding product data...')

        # Criar tags
        tag_names = ["Buquê", "Arranjo", "Ocasião Especial", "Flores Secas", "Presente"]
        tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
        tag_all = Tag.objects.get_or_create(name="all")[0]

        # Dados de exemplo
        products_data = [
            {'name': 'Buquê de Rosas Vermelhas', 'desc': 'Um clássico buquê com 12 rosas vermelhas frescas.'},
            {'name': 'Arranjo de Girassóis Alegres', 'desc': 'Arranjo vibrante para iluminar o dia de alguém.'},
            {'name': 'Cesta de Café da Manhã Especial', 'desc': 'Uma cesta completa com flores e delícias.'},
            {'name': 'Orquídea Phalaenopsis Branca', 'desc': 'Elegância e sofisticação em forma de flor.'},
            {'name': 'Mix de Flores do Campo', 'desc': 'Um buquê rústico e charmoso com flores da estação.'},
            {'name': 'Buquê de Lírios Brancos', 'desc': 'A pureza e a paz dos lírios em um lindo buquê.'},
            {'name': 'Arranjo de Flores Secas', 'desc': 'Beleza duradoura que decora qualquer ambiente.'},
            {'name': 'Mini Rosas Encantadas', 'desc': 'Pequenas rosas em um vaso delicado, perfeito para presentear.'},
            {'name': 'Buquê de Astromélias Coloridas', 'desc': 'Um buquê alegre que simboliza amizade e felicidade.'},
            {'name': 'Terrário de Suculentas', 'desc': 'Um pequeno jardim de suculentas, fácil de cuidar.'},
        ]

        for product_data in products_data:
            name = product_data['name']
            product = Product.objects.create(
                name=name,
                price=round(random.uniform(49.90, 299.90), 2),
                desc=product_data['desc'],
                size='fixed',
                term=random.randint(1, 3),
                stock=random.randint(0, 25),
                slug=slugify(name),
                firstPhoto=f'https://via.placeholder.com/400x400.png/F3E1E9/BF5B87?text={slugify(name)}'
            )

            # Adicionar tags aleatórias
            product.tags.add(*random.sample(tags, k=random.randint(1, 3)))
            product.tags.add(tag_all)
            self.stdout.write(self.style.SUCCESS(f'Successfully created product "{name}"'))

        self.stdout.write(self.style.SUCCESS('Finished seeding data.'))
