from kafka import KafkaConsumer
import json
from sqlmodel import Session
from app.database.session import sync_engine
from app.models.analytics_raw import AnalyticsRaw

consumer = KafkaConsumer(
    "requests",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="analytics-consumer-group"
)

engine = sync_engine

print("[Kafka] Consumer started. Waiting for messages...")

for message in consumer:
    data = message.value["payload"]
    print(f"[Kafka] Received: {data}")

    record = AnalyticsRaw(
        request_id=data["request_id"],
        insect_type=data["insect_type"],
        city=data["city"],
        processed_at=data["processed_at"],
        source=data["source"],
        executor=data["executor"]
    )

    with Session(engine) as session:
        session.add(record)
        session.commit()
        print(f"[Kafka] Saved to analytics_raw (request_id={record.request_id})")