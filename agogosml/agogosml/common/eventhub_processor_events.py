"""EventProcessor host class for Event Hub"""

from azure.eventprocessorhost import AbstractEventProcessor

from ..utils.logger import Logger

logger = Logger()


class EventProcessor(AbstractEventProcessor):
    """Example Implementation of AbstractEventProcessor."""

    def __init__(self, params):
        """
        Init Event processor.

        :param params: List of params.
        """
        super().__init__()
        self.on_message_received_callback = params[0]
        self._msg_counter = 0

    async def open_async(self, context):
        """
        Called by processor host to initialize the event processor.
        """
        logger.info("Connection established {}".format(context.partition_id))

    async def close_async(self, context, reason):
        """
        Called by processor host to indicate that the event processor
        is being stopped.

        :param context: Information about the partition.
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param reason: Reason for closing the async loop.
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

        :param context: Information about the partition.
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param messages: The events to be processed.
        :type messages: list[~azure.eventhub.common.EventData]
        """
        for message in messages:
            message_json = message.body_as_str(encoding='UTF-8')
            if self.on_message_received_callback is not None:
                self.on_message_received_callback(message_json)
                logger.debug("Received message: {}".format(message_json))
        logger.info("Events processed {}".format(context.sequence_number))
        await context.checkpoint_async()

    async def process_error_async(self, context, error):
        """
        Called when the underlying client experiences an error while receiving.
        EventProcessorHost will take care of recovering from the error and
        continuing to pump messages, so no external action is required.

        :param context: Information about the partition.
        :type context: ~azure.eventprocessorhost.PartitionContext
        :param error: The error that occured.
        """
        logger.error("Event Processor Error {!r}".format(error))
