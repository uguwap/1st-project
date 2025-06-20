from kafka import KafkaProducer
import json
from app.models.request import Request
from app.models.user import User

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8")
)

def send_request_completed_event(request: Request, executor: User):
    event = {
        "type": "RequestCompleted",
        "payload": {
            "request_id": request.id,
            "insect_type": request.insect_type,
            "city": request.city,
            "source": request.source,
            "processed_at": request.processed_at.isoformat() if request.processed_at else None,
            "created_at": request.created_at.isoformat() if request.created_at else None,
            "treatment": request.treatment,
            "price": request.price,
            "comment": request.comment,
            "executor_id": executor.id,
            "executor_name": executor.username,
            "executor_phone": executor.phone
        }
    }
    producer.send("requests", value=event)
    producer.flush()
