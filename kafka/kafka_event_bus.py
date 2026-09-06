
import os
import json
from datetime import datetime
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError


class KafkaEventBus:

    def __init__(self):

        self.bootstrap_servers = os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS",
            "localhost:9092"
        )

        self.producer = None

    def connect_producer(self):

        try:

            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda value:
                    json.dumps(value).encode("utf-8"),
                request_timeout_ms=3000,
            )

            return {
                "status": "connected",
                "bootstrap_servers": self.bootstrap_servers
            }

        except Exception as e:

            self.producer = None

            return {
                "status": "not_connected",
                "bootstrap_servers": self.bootstrap_servers,
                "reason": str(e)
            }

    def publish(self, topic, event):

        if self.producer is None:
            result = self.connect_producer()

            if result["status"] != "connected":
                return {
                    "status": "not_connected",
                    "topic": topic,
                    "event": event,
                    "reason": result.get("reason")
                }

        try:

            future = self.producer.send(
                topic,
                value=event
            )

            metadata = future.get(timeout=5)

            return {
                "status": "published",
                "topic": metadata.topic,
                "partition": metadata.partition,
                "offset": metadata.offset
            }

        except Exception as e:

            return {
                "status": "publish_failed",
                "topic": topic,
                "reason": str(e)
            }

    def close(self):

        if self.producer is not None:
            self.producer.close()


class KafkaEventConsumer:

    def __init__(
        self,
        topic,
        group_id="ai_identity_consumer"
    ):

        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS",
            "localhost:9092"
        )

    def create_consumer(self):

        return KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda value:
                json.loads(value.decode("utf-8")),
            consumer_timeout_ms=3000
        )
