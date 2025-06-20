from kafka.producer import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8")
)

test_event = {
    "type": "RequestCompleted",
    "payload": {
        "request_id": 777,
        "insect_type": "таракан",
        "city": "Москва",
        "processed_at": "2025-05-19T22:22:00",
        "source": "Telegram",
        "executor": "dmitry_123"
    }
}

producer.send("requests", value=test_event)
producer.flush()

print("✅ Event sent to Kafka.")