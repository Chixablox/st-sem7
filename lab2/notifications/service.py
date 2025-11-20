from confluent_kafka import Consumer
import json
import time


class NotificationService:
    def __init__(self, kafka_bootstrap: str, topic: str):
        config = {
            "bootstrap.servers": kafka_bootstrap,
            "group.id": "test-group",
            "auto.offset.reset": "earliest",
        }
        self.topic = topic
        self.consumer = Consumer(config)
        self.consumer.subscribe([self.topic])

    def listen(self):
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            data = json.loads(msg.value().decode("utf-8"))
            return data

    def close(self):
        self.consumer.close()
