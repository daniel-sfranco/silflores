import requests #type:ignore
from django.conf import settings

class PagSeguroAPI:
    BASE_URL = (
        "https://ws.sandbox.pagseguro.uol.com.br"
        if settings.PAGSEGURO_SANDBOX
        else "https://ws.pagseguro.uol.com.br"
    )

    @staticmethod
    def generate_payment(data):
        url = f"{PagSeguroAPI.BASE_URL}/v2/checkout"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        payload = {
            "email": settings.PAGSEGURO_EMAIL,
            "token": settings.PAGSEGURO_TOKEN,
            "currency": "BRL",
            **data,
        }
        response = requests.post(url, headers=headers, data=payload)
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