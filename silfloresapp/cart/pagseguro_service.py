import requests
from django.conf import settings


class PagSeguroAPI:
    BASE_URL = (
        "https://sandbox.api.pagseguro.com"
        if settings.PAGSEGURO_SANDBOX
        else "https://pagseguro.uol.com.br"
    )

    @staticmethod
    def generate_payment(cart):
        cart.status = "closed"
        cart.save()
        user = cart.user
        cep = user.cep.replace("-", "")
        address = requests.get(f"https://viacep.com.br/ws/{cep}/json").json()
        url = f"{PagSeguroAPI.BASE_URL}/checkouts"
        headers = {
            "accept": "*/*",
            "Authorization": f"Bearer {settings.PAGSEGURO_TOKEN}",
            "Content-type": "application/json"
        }
        data = {
            "customer": {
                "phone": {
                    "country": "+55",
                    "area": str(user.ddd),
                    "number": str(user.phone),
                },
                "Name": user.name,
                "email": user.email,
                "tax_id": user.cpf,
            },
            "shipping": {
                "address": {
                    "street": address["logradouro"],
                    "number": str(user.home_number),
                    "city": address["localidade"],
                    "region_code": address["uf"],
                    "country": "BRA",
                    "postal_code": user.cep,
                    "complement": user.complement or "Não se aplica",
                    "locality": address["bairro"]
                },
                "box": {
                    "dimensions": {
                        "length": 16,
                        "width": 11,
                        "height": 3
                    },
                    "weight": 300
                },
                "type": "FIXED",
                "address_modifiable": False,
                "amount": cart.freightValue * 100,
            },
            "customer_modifiable": True,
            "reference_id": cart.id,
            "items": [],
            "payment_methods": [
                {"type": "CREDIT_CARD"},
                {"type": "DEBIT_CARD"},
                {"type": "BOLETO"},
                {"type": "PIX"}],
        }
        if settings.DEBUG:
            data['redirect_url'] = f'{settings.NGROK_URL}/cart/thanks'
        else:
            data['redirect_url'] = "https://silflores.com.br/cart/thanks"
        for cartitem in cart.items.all():
            item = {}
            item['reference_id'] = cartitem.product.id
            item['name'] = cartitem.product.name
            item['quantity'] = cartitem.quantity
            item['unit_amount'] = int(cartitem.product.price * 100)
            item['image_url'] = cartitem.product.firstPhoto.url
            data['items'].append(item)
        response = requests.post(url, headers=headers, json=data)
        print(response.json())
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
