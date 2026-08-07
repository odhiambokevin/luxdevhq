import json
from kafka import KafkaConsumer

TOPIC = "kenya_weather"
BOOTSTRAP_SERVERS = "kafka:9092"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="weather-debug-002",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print("Waiting for weather forecasts...\n")

for message in consumer:
    print("Received:")
    print(json.dumps(message.value, indent=4),flush=True)