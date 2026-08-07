import json
import random
import time
from datetime import datetime, timedelta
from faker import Faker
from kafka import KafkaProducer

faker = Faker()

TOPIC = "kenya_transactions"

producer = KafkaProducer(bootstrap_servers="kafka:9092",value_serializer=lambda x: json.dumps(x).encode("utf-8"))

branches = [
    "Upper Hill",
    "Westlands",
    "Mombasa",
    "Kisumu",
    "Nakuru",
    "Eldoret",
    "Kericho",
    "Thika"
]

#create 100 reusable customer accounts to simulate real world data
accounts = {}

NUM_CUSTOMERS = 100

for _ in range(NUM_CUSTOMERS):
    account_number = str(faker.random_number(digits=10, fix_len=True)) 

    accounts[account_number] = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "branch": random.choice(branches),
        "customer_city": faker.city(),
        "balance": round(random.uniform(5000, 150000), 2)
    }

#transactions
current_time = datetime.now()

NUM_TRANSACTIONS = 500

for _ in range(NUM_TRANSACTIONS):

    #pick random existing customer
    account_number = random.choice(list(accounts.keys()))

    customer = accounts[account_number]
    opening_balance = customer["balance"]
    transaction_type = random.choice(["deposit", "withdrawal"])
    amount = round(random.uniform(100, 30000), 2)

    if transaction_type == "deposit":
        closing_balance = opening_balance + amount
        status = "success"
    else:
        if amount <= opening_balance:
            closing_balance = opening_balance - amount
            status = "success"
        else:
            closing_balance = opening_balance
            status = "failed - Insufficient Funds"

    #update customer balance only if transaction succeeds
    if status == "success":
        customer["balance"] = closing_balance

    transaction = {
        "first_name": customer["first_name"],
        "last_name": customer["last_name"],
        "account_number": account_number,
        "branch": customer["branch"],
        "customer_city": customer["customer_city"],
        "transaction": transaction_type,
        "amount": amount,
        "opening_balance": round(opening_balance, 2),
        "closing_balance": round(customer["balance"], 2),
        "status": status,
        "transacted": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }

    producer.send(TOPIC, transaction)

    print("-" * 45)
    print(json.dumps(transaction, indent=4))

    #simulated time of next transaction by 5–10 minutes
    current_time += timedelta(minutes=random.randint(5, 10))

    #slow down producer
    time.sleep(2)

producer.flush()
producer.close()