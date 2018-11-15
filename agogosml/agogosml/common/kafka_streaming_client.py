"""Kafka streaming client"""

from .abstract_streaming_client import AbstractStreamingClient
from confluent_kafka import Producer, Consumer, admin
from confluent_kafka import KafkaException, KafkaError
import sys
import logging

logger = logging.getLogger("STREAM")
logger.setLevel(logging.INFO)


class KafkaStreamingClient(AbstractStreamingClient):

    def __init__(self, config):
        """
        Class to create a kafka streaming client instance.

        Args:
            config: dictionary file with all the relevant parameters
            topic: A string kafka topic.
        """

        self.topic = config.get("KAFKA_TOPIC")

        kafka_config = self.create_kafka_config(config)
        self.admin = admin.AdminClient(kafka_config)

        if config.get("KAFKA_CONSUMER_GROUP") is None:
            self.producer = Producer(kafka_config)
        else:
            self.app_host = config.get("APP_HOST")
            self.app_port = config.get("APP_PORT")
            self.consumer = Consumer(kafka_config)

    @staticmethod
    def create_kafka_config(user_config):

        config = {
            "bootstrap.servers": user_config.get("KAFKA_ADDRESS"),
            "enable.auto.commit": False,
            "auto.offset.reset": "earliest"
        }

        consumer_group = user_config.get("KAFKA_CONSUMER_GROUP")
        if consumer_group is not None:
            config["group.id"] = consumer_group

        return config

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """

        if err is not None:
            logger.error('Message delivery failed: {}'.format(err))
        else:
            logger.info('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def send(self, message: str, *args, **kwargs):
        """
        Upload a message to a kafka topic.

        Args:
            message: A string input to upload to kafka.
        """
        if not isinstance(message, str):
            raise TypeError('str type expected for message')
        mutated_message = message.encode('utf-8')
        self.producer.poll(0)
        self.producer.produce(self.topic, mutated_message, callback=self.delivery_report)
        self.producer.flush()

    def stop(self, *args, **kwargs):
        pass

    def start_receiving(self, on_message_received_callback):
        """
        Receive messages from a kafka topic.
        """
        '''
        TODO:
        We are going to need documentation for Kafka
        to ensure proper syntax is clear
        '''
        self.consumer.subscribe([self.topic])
        # Read messages from Kafka, print to stdout
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    # Error or event
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        logger.error(
                            '%% %s [%d] reached end at offset %d\n' %
                            (msg.topic(), msg.partition(), msg.offset()))
                    else:
                        # Error
                        raise KafkaException(msg.error())
                else:
                    # Proper message
                    on_message_received_callback(msg.value())
                    self.consumer.commit(msg)

        except KeyboardInterrupt:
            sys.stderr.write('%% Aborted by user\n')

        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()
