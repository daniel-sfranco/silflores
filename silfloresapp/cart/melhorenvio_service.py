import os
import urllib.parse
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.utils import timezone
from pyppeteer import launch

from .models import MelhorEnvioToken


class MelhorEnvioAPI:
    def __init__(self, superuser: bool, check=True):
        instance = MelhorEnvioToken.objects.get(sandbox=settings.MELHOR_ENVIO_SANDBOX)
        self.client_id = settings.MELHOR_ENVIO_ID
        self.client_secret = settings.MELHOR_ENVIO_SECRET
        self.token_url = settings.MELHOR_ENVIO_LINK + '/oauth/token'
        self.api_url = settings.MELHOR_ENVIO_LINK + '/api/v2'
        self.token = instance.access_token
        self.state = "randomstring123"
        self.scope = 'cart-read cart-write companies-read companies-write coupons-read coupons-write notifications-read orders-read products-read products-write purchases-read shipping-calculate shipping-cancel shipping-checkout shipping-companies shipping-generate shipping-preview shipping-print shipping-share shipping-tracking ecommerce-shipping users-read users-write'
        self.expires_in = instance.expires_in
        self.check_token(superuser)

    def check_token(self, superuser: bool):
        url = f"{self.api_url}/me"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            remainingTime = self.expires_in - timedelta(days=7)
            if remainingTime < timezone.now():
                print("Token prestes a expirar")
            return True
        else:
            raise Exception(f"Erro inesperado: {response.status_code} - {response.text}")

    def calculate_shipping(self, user):
        self.check_token(user.is_superuser)
        payload = {
            "from": { "postal_code": f"{settings.ADMIN_CEP}" },
            "to": { "postal_code": f"{user.cep}" },
            "package": {
                "height": 6,
                "width": 16,
                "length": 18,
                "weight": 0.3
            },
            "options": {
                "insurance_value": f"{user.cart.fullPrice}",
                "receipt": False,
                "own_hand": False
            }
        }
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'User-Agent': 'danielsfranco346@gmail.com'
        }
        url = f'{self.api_url}/me/shipment/calculate'
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Falha ao calcular frete. Código: {response.status_code}. Corpo: {response.json()}')

    def add_to_cart(self, user):
        self.check_token(user.is_superuser)
        cep = user.cep.replace("-", "")
        address = requests.get(f"https://viacep.com.br/ws/{cep}/json").json()
        payload = {
            "service": f"{user.cart.freightOption}",
            "from": {
                "name": os.getenv('ADMIN_NAME', 'change-me'),
                "phone": os.getenv('ADMIN_PHONE', 'change-me'),
                "email": os.getenv('ADMIN_EMAIL', 'change-me'),
                "document": os.getenv('ADMIN_CPF', '0'),
                #"company_document": os.getenv('ADMIN_CNPJ', 'change-me'),
                "state_register": os.getenv('ADMIN_STATE_REGISTER', 'change-me'),
                "address": os.getenv('ADMIN_ADDRESS', 'change-me'),
                "complement": os.getenv('ADMIN_COMPLEMENT', 'change-me'),
                "number": os.getenv('ADMIN_HOME_NUMBER', 'change-me'),
                "district": os.getenv('ADMIN_DISTRICT', 'change-me'),
                "city": os.getenv('ADMIN_CITY', 'change-me'),
                "state_abbr": os.getenv('ADMIN_UF', 'change-me'),
                "country_id": os.getenv('ADMIN_COUNTRY', 'change-me'),
                "postal_code": os.getenv('ADMIN_CEP')
            },
            "to": {
                "name": f"{user.name}",
                "phone": f"{user.phone}",
                "email": f"{user.email}",
                "document": f"{user.cpf}",
                "address": address['logradouro'],
                "complement": f"{user.complement or 'none'}",
                "number": f"{user.home_number}",
                "district": address['bairro'],
                "city": address['localidade'],
                "state_abbr": address['uf'],
                "country_id": "BR",
                "postal_code": f"{cep}",
                },
            "products": [],
            "options": {
                "insurance_value": f"{user.cart.fullPrice}",
                "receipt": False,
                "own_hand": False,
                "reverse": False,
                "non_commercial": True,
                #"invoice": { "key": "string" },
                "plataform": "Silflores Acessórios",
                "tags": []
            }
        }
        if(user.cart.freightOption <= 2 or user.cart.freightOption > 4):
            payload["package"] = {
                "weight": 0.3,
                "width": 18,
                "height": 8,
                "length": 27,
            }
        else:
            payload["volumes"] = [{
                "weight": 0.3,
                "width": 16,
                "height": 6,
                "length": 18,
            }]

        cart = user.cart
        for item in cart.items.all():
            product = {
                "name": item.product.name,
                "quantity": int(item.quantity),
                "unitary_value": float(item.product.price),
            }
            payload['products'].append(product)

        url = f"{self.api_url}/me/cart"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"Aplicação {settings.ADMIN_EMAIL}"
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def buy_shipments(self, id):
        url=f"{self.api_url}/me/shipment/checkout"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"Aplicação {settings.ADMIN_EMAIL}"
        }
        payload={
            'orders': [id]
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        if response.status_code < 400:
            return response.json()
        raise Exception("Failed to pay shipments" + response.text)

    def generate_labels(self, shipmentId):
        url=f"{self.api_url}/me/shipment/generate"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"Aplicação {settings.ADMIN_EMAIL}"
        }
        payload={
            'orders': [shipmentId]
        }
        response = requests.post(url, headers=headers, json=payload)
        url=f"{self.api_url}/me/shipment/print"
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code < 400:
            return response.json()
        raise Exception("Failed to generate labels" + response.text)

    def track_shipment(self, user, shipmentId):
        self.check_token(user.is_superuser)
        url = f"{self.api_url}/me/shipment/track/{shipmentId}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"Aplicação {settings.ADMIN_EMAIL}"
        }
        response = requests.post(url, headers=headers)
        print(response.json())
        print(response.status_code)
        if response.status_code < 400:
            return response.json()
        raise Exception("Failed to track shipment" + response.text)


async def generate_pdf_from_url(url, token=None):
    browser = await launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox'],
        executablePath='/usr/bin/chromium-browser',
    )
    page = await browser.newPage()
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        await page.setExtraHTTPHeaders(headers)
    await page.goto(url, {"waitUntil": "networkidle2"})
    pdf = await page.pdf({
        "format": "A4",
        "printBackground": True,
        "margin": {"top": "0mm", "left": "0mm", "bottom": "0mm", "rignt": "0mm"}
    })
    await browser.close()
    return pdf
