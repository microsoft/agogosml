"""Kafka streaming client"""

from datetime import datetime

from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from confluent_kafka import Producer
from confluent_kafka import admin

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.utils.logger import Logger


class KafkaStreamingClient(AbstractStreamingClient):
    """Kafka streaming client"""

    def __init__(self, config):  # pragma: no cover
        """
        Streaming client implementation based on Kafka.

        Configuration keys:
          KAFKA_ADDRESS
          KAFKA_CONSUMER_GROUP
          KAFKA_TOPIC
          TIMEOUT
          EVENTHUB_KAFKA_CONNECTION_STRING
        """
        self.logger = Logger()

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
            self.logger.info('Creating Producer')
            self.producer = Producer(kafka_config)
        else:
            self.logger.info('Creating Consumer')
            self.consumer = Consumer(kafka_config)

    @staticmethod
    def create_kafka_config(user_config: dict) -> dict:  # pragma: no cover
        """Creates the kafka configuration"""
        config = {
            "bootstrap.servers": user_config.get("KAFKA_ADDRESS"),
            "enable.auto.commit": False,
            "auto.offset.reset": "latest",
            "default.topic.config": {'auto.offset.reset': 'latest'},
        }

        if user_config.get('KAFKA_CONSUMER_GROUP') is not None:
            config['group.id'] = user_config['KAFKA_CONSUMER_GROUP']

        if user_config.get('KAFKA_DEBUG') is not None:
            config['debug'] = user_config['KAFKA_DEBUG']

        if user_config.get('EVENTHUB_KAFKA_CONNECTION_STRING'):
            ssl_location = user_config.get('SSL_CERT_LOCATION') or '/etc/ssl/certs/ca-certificates.crt'
            eventhub_config = {
                'security.protocol': "SASL_SSL",
                'sasl.mechanism': "PLAIN",
                'ssl.ca.location': ssl_location,
                'sasl.username': '$ConnectionString',
                'sasl.password': user_config.get('EVENTHUB_KAFKA_CONNECTION_STRING'),
                'client.id': 'agogosml',
            }

            config = {**config, **eventhub_config}

        return config

    def delivery_report(self, err, msg):  # pragma: no cover
        """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush().

        :param err: An error message.
        :param msg: A string input to be uploaded to kafka.
        """

        if err is not None:
            self.logger.error('Message delivery failed: %s', err)
        else:
            self.logger.info('Message delivered to %s [%s]',
                             msg.topic(), msg.partition())

    def send(self, message: str):  # pragma: no cover
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        try:
            mutated_message = message.encode('utf-8')
            self.logger.info('Sending message to kafka topic: %s', self.topic)
            self.producer.poll(0)
            self.producer.produce(
                self.topic, mutated_message, callback=self.delivery_report)
            self.producer.flush()
            return True
        except Exception as ex:
            self.logger.error('Error sending message to kafka: %s', ex)
            return False

    def stop(self):  # pragma: no cover
        pass

    def check_timeout(self, start: datetime):  # pragma: no cover
        """Interrupts if too much time has elapsed since the kafka client started running."""
        if self.timeout is not None:
            elapsed = datetime.now() - start
            if elapsed.seconds >= self.timeout:
                raise KeyboardInterrupt

    def handle_kafka_error(self, msg):  # pragma: no cover
        """Handle an error in kafka."""
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event
            self.logger.info('%% %s [%d] reached end at offset %d\n',
                             msg.topic(), msg.partition(), msg.offset())
        else:
            # Error
            raise KafkaException(msg.error())

    def start_receiving(self, on_message_received_callback):  # pragma: no cover
        try:
            self.subscribe_to_topic()
            start = datetime.now()

            while True:
                # Stop loop after timeout if exists
                self.check_timeout(start)

                # Poll messages from topic
                msg = self.read_single_message()
                if msg is not None:
                    on_message_received_callback(msg)

        except KeyboardInterrupt:
            self.logger.info('Aborting listener...')

        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    def subscribe_to_topic(self):  # pragma: no cover
        """Subscribe to topic"""
        self.consumer.subscribe([self.topic])

    def read_single_message(self):  # pragma: no cover
        """Poll messages from topic"""
        msg = self.consumer.poll(0.000001)

        if msg is None:
            return None

        if msg.error():
            # Error or event
            self.handle_kafka_error(msg)
            return None

        # Proper message
        # self.logger.info('kafka read message: %s, from topic: %s', msg.value(), msg.topic())
        self.consumer.commit(msg)
        return msg.value()
