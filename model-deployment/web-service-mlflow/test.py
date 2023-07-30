import requests

def send_request(credit_card):
    url = 'http://localhost:9696/predict'
    response = requests.post(url, json=credit_card)
    print(response.json())

credit_cards = [
    {
        'duration': 60, 
        'credit_amount': 1000, 
        'installment_commitment': 10, 
        'residence_since': 10,
        'age': 30, 
        'existing_credits': 50, 
        'num_dependents': 2
    },
    {
         "duration": 81,
         "credit_amount": 3893,
         "installment_commitment": 4,
         "residence_since": 11,
         "age": 64,
         "existing_credits": 100,
         "num_dependents": 3
    },
    {
    "duration": 120,
    "credit_amount": 5000,
    "installment_commitment": 1,
    "residence_since": 1,
    "age": 18,
    "existing_credits": 100,
    "num_dependents": 5
}
]

for credit_card in credit_cards:
    send_request(credit_card)