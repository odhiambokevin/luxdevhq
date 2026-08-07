import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "kenya_transactions",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="bank-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Waiting for transactions...\n")

for message in consumer:
    transaction = message.value

    print("-" * 45)
    print(f"Customer          : {transaction['first_name']} {transaction['last_name']}")
    print(f"Account Number    : {transaction['account_number']}")
    print(f"Branch            : {transaction['branch']}")
    print(f"City              : {transaction['customer_city']}")
    print(f"Transaction Type  : {transaction['transaction']}")
    print(f"Amount            : {transaction['amount']}")
    print(f"Opening Balance   : {transaction['opening_balance']}")
    print(f"Closing Balance   : {transaction['closing_balance']}")
    print(f"Status            : {transaction['status']}")
    print(f"Transaction Time  : {transaction['transacted']}")