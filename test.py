import requests

# L'URL de l'API
url = "https://codemed-production.up.railway.app/generate-code"

# Le prompt que vous souhaitez envoyer à l'API
data = {
    "prompt": "def addtonumbers(a: float, b: float):\n    '''Return the sum of two numbers.'''"
}

# Effectuer la requête POST
response = requests.post(url, json=data)

# Vérifier le statut de la réponse
if response.status_code == 200:
    generated_code = response.json()['generated_code']
    print("Generated code:", generated_code)
else:
    print("Error:", response.status_code, response.text)
