import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orders.model import Base
from orders.model import Order
from orders.service import OrderService
from notifications.service import NotificationService
from orderFactory import OrderFactory
import time


def test():
    with PostgresContainer("postgres:16") as postgres, KafkaContainer(
        "confluentinc/cp-kafka:7.5.0"
    ) as kafka:
        kafka_bootstrap = kafka.get_bootstrap_server()
        topic = "orders"

        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        with Session() as session:
            test_order = OrderFactory.build()

            order_service = OrderService(session, kafka_bootstrap, topic)
            time.sleep(5)
            created_order = order_service.create_order(
                test_order.item_name, test_order.quantity
            )

            db_order = session.get(Order, created_order.id)
            assert db_order.item_name == test_order.item_name
            assert db_order.quantity == test_order.quantity

            notification_service = NotificationService(kafka_bootstrap, topic)
            time.sleep(5)
            message = notification_service.listen()
            notification_service.close()

            assert message is not None
            assert message["id"] == created_order.id
            assert message["item_name"] == created_order.item_name
            assert message["quantity"] == created_order.quantity
