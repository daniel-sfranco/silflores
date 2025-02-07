import requests #type:ignore
from django.conf import settings

class PagSeguroAPI:
    BASE_URL = (
        "https://sandbox.api.pagseguro.com"
        if settings.PAGSEGURO_SANDBOX
        else "https://pagseguro.uol.com.br"
    )

    @staticmethod
    def generate_payment(data):
        url = f"{PagSeguroAPI.BASE_URL}/checkouts"
        headers = {
            "accept": "*/*",
            "Authorization": f"Bearer {settings.PAGSEGURO_TOKEN}",
            "Content-type": "application/json"
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_transaction_details(transaction_code):
        url = f"{PagSeguroAPI.BASE_URL}/v2/transactions/{transaction_code}"
        params = {
            "email": settings.PAGSEGURO_EMAIL,
            "token": settings.PAGSEGURO_TOKEN,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()