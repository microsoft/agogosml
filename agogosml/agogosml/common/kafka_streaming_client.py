"""Kafka streaming client"""

import datetime

from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from confluent_kafka import Producer
from confluent_kafka import admin

from ..utils.logger import Logger
from .abstract_streaming_client import AbstractStreamingClient

logger = Logger()


class KafkaStreamingClient(AbstractStreamingClient):
    def __init__(self, config):
        """
        Streaming client implementation based on Kafka.

        Configuration keys:
          KAFKA_ADDRESS
          KAFKA_CONSUMER_GROUP
          KAFKA_TOPIC
          TIMEOUT
          EVENTHUB_KAFKA_CONNECTION_STRING
        """

        self.topic = config.get("KAFKA_TOPIC")
        if config.get("TIMEOUT"):
            try:
                self.timeout = int(config.get("TIMEOUT"))
            except ValueError:
                self.timeout = None
        else:
            self.timeout = None

        kafka_config = self.create_kafka_config(config)
        self.admin = admin.AdminClient(kafka_config)

        if config.get("KAFKA_CONSUMER_GROUP") is None:
            self.producer = Producer(kafka_config)
        else:
            self.consumer = Consumer(kafka_config)

    @staticmethod
    def create_kafka_config(user_config: dict) -> dict:
        """Creates the kafka configuration"""
        config = {
            "bootstrap.servers": user_config.get("KAFKA_ADDRESS"),
            "enable.auto.commit": False,
            "auto.offset.reset": "earliest",
            # 'request.timeout.ms': 60000,
            # 'session.timeout.ms': 60000,
            # 'default.topic.config': {'auto.offset.reset': 'smallest'},
        }

        if user_config.get('EVENTHUB_KAFKA_CONNECTION_STRING'):
            eventhub_config = {
                'security.protocol': "SASL_SSL",
                'sasl.mechanism': "PLAIN",
                'ssl.ca.location': '/usr/local/etc/openssl/cert.pem',
                'sasl.username': '$ConnectionString',
                'sasl.password': user_config.get('EVENTHUB_KAFKA_CONNECTION_STRING'),
                'client.id': 'agogosml',
            }
            config = {**config, **eventhub_config}

        consumer_group = user_config.get("KAFKA_CONSUMER_GROUP")
        if consumer_group is not None:
            config["group.id"] = consumer_group

        return config

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush().

        :param err: An error message.
        :param msg: A string input to be uploaded to kafka.
        """

        if err is not None:
            logger.error('Message delivery failed: %s', err)
        else:
            logger.info('Message delivered to %s [%s]',
                        msg.topic(), msg.partition())

    def send(self, message: str):
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        try:
            mutated_message = message.encode('utf-8')
            self.producer.poll(0)
            self.producer.produce(
                self.topic, mutated_message, callback=self.delivery_report)
            self.producer.flush()
            return True
        except Exception as e:
            logger.error('Error sending message to kafka: %s', e)
            return False

    def stop(self, *args, **kwargs):
        pass

    def check_timeout(self, start: datetime.datetime):
        """Interrupts if too much time has elapsed since the kafka client started running."""
        if self.timeout is not None:
            elapsed = datetime.datetime.now() - start
            if elapsed.seconds >= self.timeout:
                raise KeyboardInterrupt

    def handle_kafka_error(self, msg):
        """Handle an error in kafka."""
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event
            logger.error('%% %s [%d] reached end at offset %d\n',
                         msg.topic(), msg.partition(), msg.offset())
        else:
            # Error
            raise KafkaException(msg.error())

    def start_receiving(self, on_message_received_callback):
        # TODO: We are going to need documentation for Kafka to ensure proper syntax is clear
        try:
            self.subscribe_to_topic()
            start = datetime.datetime.now()

            while True:
                # Stop loop after timeout if exists
                self.check_timeout(start)

                # Poll messages from topic
                msg = self.read_single_message()
                if msg is not None:
                    on_message_received_callback(msg)

        except KeyboardInterrupt:
            logger.info('Aborting listener...')

        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    def subscribe_to_topic(self):
        """Subscribe to topic"""
        self.consumer.subscribe([self.topic])

    def read_single_message(self):
        """Poll messages from topic"""
        msg = self.consumer.poll(0.000001)
        if msg is None:
            return None
        if msg.error():
            # Error or event
            self.handle_kafka_error(msg)
            return None
        else:
            # Proper message
            # logger.info('kafka read message: %s, from topic: %s', msg.value(), msg.topic())
            self.consumer.commit(msg)
            return msg.value()
