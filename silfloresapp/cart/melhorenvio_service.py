import requests
from django.conf import settings

class MelhorEnvioAPI:
    def __init__(self):
        self.client_id = settings.MELHOR_ENVIO_CLIENT_ID
        self.client_secret = settings.MELHOR_ENVIO_CLIENT_SECRET
        self.token_url = settings.MELHOR_ENVIO_LINK + '/oauth/token'
        self.api_url = settings.MELHOR_ENVIO_LINK + '/api/v2/'

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

    def freight_calc(self, payload):
        token = settings.MELHOR_ENVIO_TOKEN
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'danielsfranco346@gmail.com'
        }
        url = f'{self.api_url}me/shipment/calculate'
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Falha ao calcular frete')

