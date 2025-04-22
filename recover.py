import requests

url = "https://melhorenvio.com.br/oauth/token"
payload = {
    "grant_type": "authorization_code",
    "client_id": "5602",
    "client_secret": "ZysdKWVD5kR1GjSa9bimMefzhTU39RyfnNBUBh1J",
    "redirect_uri": "https://9f21-189-111-174-72.ngrok-free.app/thanks",
    "code": "CODIGO_DE_AUTORIZACAO"
}
response = requests.post(url, data=payload)
tokens = response.json()

print(tokens)