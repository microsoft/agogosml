"""EventProcessor host class for Event Hub"""

from azure.eventprocessorhost import AbstractEventProcessor, AzureStorageCheckpointLeaseManager, \
            EventHubConfig, EventProcessorHost, EPHOptions
import asyncio
import logging
import requests
import os

logger = logging.getLogger('logger')

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

class EventProcessor(AbstractEventProcessor):
    """
    Example Implementation of AbstractEventProcessor
    """

    def __init__(self, params=None):
        """
        Init Event processor
        """
        super().__init__(params)
        self._msg_counter = 0

    async def open_async(self, context):
        """
        Called by processor host to initialize the event processor.
        """
        logger.info("Connection established {}".format(context.partition_id))

    async def close_async(self, context, reason):
        """
        Called by processor host to indicate that the event processor is being stopped.
        :param context: Information about the partition
        :type context: ~azure.eventprocessorhost.PartitionContext
        """
        logger.info("Connection closed (reason {}, id {}, offset {}, sq_number {})".format(
            reason,
            context.partition_id,
            context.offset,
            context.sequence_number))

    async def process_events_async(self, context, messages):
        """TODO: Need to iterate through each message in messages and make an http request
        to the sample app. This looks to be writing the messages?!"""
        """
        Called by the processor host when a batch of events has arrived.
        This is where the real work of the event processor is done.
        :param context: Information about the partition
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param messages: The events to be processed.
        :type messages: list[~azure.eventhub.common.EventData]
        """
        for message in messages:
            message_json = message.body_as_json(encoding='UTF-8')
            # TODO: fix endpoint passing and add checks for data format
            server_address = (HOST, int(PORT))
            request = requests.post(server_address, data=message_json)
            if request.status_code != 200:
                logger.info("Error with a request {} and message not sent was {}".format(
                    request.status_code, message_json))
            # TODO: Need to log every however many messages, cant be after all of them.
        logger.info("Events processed {}".format(context.sequence_number))
        await context.checkpoint_async()

    async def process_error_async(self, context, error):
        """
        Called when the underlying client experiences an error while receiving.
        EventProcessorHost will take care of recovering from the error and
        continuing to pump messages,so no action is required from
        :param context: Information about the partition
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param error: The error that occured.
        """
        logger.error("Event Processor Error {!r}".format(error))


async def wait_and_close(host):
    """
    Run EventProcessorHost for 2 minutes then shutdown.
    """
    await asyncio.sleep(10)#60
    await host.close_async()
