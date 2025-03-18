import os
import requests
from django.conf import settings
from users.models import CustomUser

class MelhorEnvioAPI:
    def __init__(self):
        self.client_id = settings.MELHOR_ENVIO_CLIENT_ID
        self.client_secret = settings.MELHOR_ENVIO_CLIENT_SECRET
        self.token_url = settings.MELHOR_ENVIO_LINK + '/oauth/token'
        self.api_url = settings.MELHOR_ENVIO_LINK + '/api/v2'
        self.token = settings.MELHOR_ENVIO_TOKEN

    def get_access_token(self):
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'cart-read cart-write companies-read companies-write coupons-read coupons-write notifications-read orders-read products-read products-write purchases-read shipping-calculate shipping-cancel shipping-checkout shipping-companies shipping-generate shipping-preview shipping-print shipping-share shipping-tracking ecommerce-shipping users-read users-write',
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "danielsfranco346@gmail.com"
        }
        response = requests.post(self.token_url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception('Falha ao obter token de acesso')

    def calculate_shipping(self, user):
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
                "insurance_value": f"user.cart.fullPrice",
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
            raise Exception('Falha ao calcular frete')

    def add_to_cart(self, user):
        cep = user.cep.replace("-", "")
        address = requests.get(f"https://viacep.com.br/ws/{cep}/json").json()
        payload = {
            "service": f"{int(user.cart.freightOption == 'SEDEX') + 1}",
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
                "complement": f"{user.complement}",
                "number": f"{user.home_number}",
                "district": address['bairro'],
                "city": address['localidade'],
                "state_abbr": address['uf'],
                "country_id": "BR",
                "postal_code": f"{cep}",
                "note": "string"
            },
            "products": [],
            "package": {
                "weight": "0.3",
                "width": "18",
                "height": "8",
                "length": "27",
            },
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

        cart = user.cart
        for item in cart.items:
            product = {
                "description": item.product.name,
                "quantity": item.quantity,
                "price": item.product.price,
                "weight": 1
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
        if response.status_code < 400:
            return response.json()
        raise Exception("Failed to create shipment")

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
        raise Exception("Failed to pay shipments")


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
        raise Exception("Failed to generate labels")

    def track_shipment(self, shipmentId):
        url=f"{self.api_url}/me/shipment/track/{shipmentId}"
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
        raise Exception("Failed to track shipment")
