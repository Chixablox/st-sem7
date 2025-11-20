import pytest
import time
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orders.model import Base


@pytest.fixture(scope="function")
def postgres_container():
    with PostgresContainer("postgres:16") as postgres:
        yield postgres


@pytest.fixture(scope="function")
def kafka_container():
    with KafkaContainer("confluentinc/cp-kafka:7.5.0") as kafka:
        time.sleep(5)
        yield kafka


@pytest.fixture(scope="function")
def engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def session(engine):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        yield session
        session.rollback()

