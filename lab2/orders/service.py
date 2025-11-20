import json
from confluent_kafka import Producer
from .model import Order
from sqlalchemy.orm import Session


class OrderService:
    def __init__(self, db_session, kafka_bootstrap: str, topic: str):
        self.session = db_session
        config = {"bootstrap.servers": kafka_bootstrap}
        self.producer = Producer(config)
        self.topic = topic

    def add_and_push_order(self, order: Order):
        self.session.add(order)
        self.session.commit()

        message = json.dumps(
            {"id": order.id, "item_name": order.item_name, "quantity": order.quantity}
        ).encode("utf-8")

        self.producer.produce(self.topic, message)
        self.producer.flush()
