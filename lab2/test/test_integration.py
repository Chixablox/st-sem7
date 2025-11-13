import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
from orders.model import Order
from orders.service import OrderService
from notifications.service import NotificationService
from orderFactory import OrderFactory


def test_create_order(db_session, kafka_container):
    topic = "orders"
    kafka_bootstrap = kafka_container.get_bootstrap_server()

    test_order = OrderFactory.build()

    order_service = OrderService(db_session, kafka_bootstrap, topic)
    created_order = order_service.create_order(
        test_order.item_name, test_order.quantity
    )

    db_order = db_session.get(Order, created_order.id)
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