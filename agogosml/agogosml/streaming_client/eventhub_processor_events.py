"""EventProcessor host class for Event Hub"""

from azure.eventprocessorhost import AbstractEventProcessor
import logging
import requests

logger = logging.getLogger("EH")
logger.setLevel(logging.INFO)

class EventProcessor(AbstractEventProcessor):
    """
    Example Implementation of AbstractEventProcessor
    """
    app_host = ""
    app_port = ""

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
        :param reason: Reason for closing the async loop
        :type reason: string
        """
        logger.info(
            "Connection closed (reason {}, id {}, offset {}, sq_number {})".
            format(reason, context.partition_id, context.offset,
                   context.sequence_number))

    async def process_events_async(self, context, messages):
        """
        Called by the processor host when a batch of events has arrived.
        This is where the real work of the event processor is done.
        :param context: Information about the partition
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param messages: The events to be processed.
        :type messages: list[~azure.eventhub.common.EventData]
        """
        for message in messages:
            try:
                message_str = message.body_as_str(encoding='UTF-8')
                server_address = (self.app_host, int(self.app_port))
                request = requests.post(server_address, data=message_str)
                if request.status_code != 200:
                    logger.error(
                        "Error with a request {} and message not sent was {}".
                        format(request.status_code, message_str))
            except:
                pass
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
