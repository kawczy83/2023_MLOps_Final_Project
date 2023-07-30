import requests

def send_request(credit_card):
    url = 'http://localhost:9696/predict'
    response = requests.post(url, json=credit_card)
    print(response.json())

credit_cards = [
    {
        "credit_amount": 2096,
        "age": 50.0,
        "checking_status": '<0',
        "duration": 100
    },
    {
        "credit_amount": 5000,
        "age": 35.0,
        "checking_status": '>=200',
        "duration": 24
    },
    {
        "credit_amount": 10000,
        "age": 27.0,
        "checking_status": '0<=X<200',
        "duration": 60
    }
]

for credit_card in credit_cards:
    send_request(credit_card)