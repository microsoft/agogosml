"""Redis streaming client"""
from typing import Optional

from redis import Redis
from redis.client import PubSubWorkerThread

from agogosml.common.abstract_streaming_client import AbstractStreamingClient


class RedisStreamingClient(AbstractStreamingClient):
    """Redis streaming client"""

    def __init__(self, config):
        """
        Redis streaming client implementation.

        Configuration keys:
            REDIS_URL
            REDIS_CHANNEL
            REDIS_SLEEP_TIME

        """
        self.channel = config['REDIS_CHANNEL']
        self.sleep_time = config.get('REDIS_SLEEP_TIME', 0.1)
        self.redis = Redis.from_url(config['REDIS_URL'])
        self.receiver_thread: Optional[PubSubWorkerThread] = None

    def start_receiving(self, on_message_received_callback):
        def on_redis_message(redis_envelope: dict):
            message = redis_envelope.get('data')
            if message:
                on_message_received_callback(message.decode('utf-8'))

        pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe(**{self.channel: on_redis_message})
        self.receiver_thread = pubsub.run_in_thread(sleep_time=self.sleep_time)

    def send(self, message):
        self.redis.publish(self.channel, message)
        return True

    def stop(self):
        if self.receiver_thread:
            self.receiver_thread.stop()
