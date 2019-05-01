"""Event Hub Streaming Class Unit Tests"""

from unittest.mock import patch

from azure.eventprocessorhost import EPHOptions
from agogosml.common.eventhub_streaming_client import EventHubStreamingClient


@patch('agogosml.utils.logger.Logger')
def test_create_eventhub_eph_options(mock_logger):
    """Test the create eventhub eph options method."""

    # Pass in empty config
    eph_options = EventHubStreamingClient.create_eventhub_eph_options({}, mock_logger)

    # Assert default config is returned.
    assert isinstance(eph_options, EPHOptions)
    assert not eph_options.debug_trace

    # Pass in null config
    config = {
        'EVENT_HUB_EPH_OPTIONS': None
    }
    eph_options = EventHubStreamingClient.create_eventhub_eph_options(config, mock_logger)
    # Assert default config is returned.
    assert isinstance(eph_options, EPHOptions)
    assert not eph_options.debug_trace

    # Pass in invalid string
    config = {
        'EVENT_HUB_EPH_OPTIONS': 'invalid'
    }
    eph_options = EventHubStreamingClient.create_eventhub_eph_options(config, mock_logger)
    # Assert default config is returned.
    assert mock_logger.warning.called
    assert isinstance(eph_options, EPHOptions)
    assert not eph_options.debug_trace

    mock_logger.reset_mock()

    # Pass in invalid string and valid debug variable
    config = {
        'EVENT_HUB_EPH_OPTIONS': 'invalid',
        'EVENT_HUB_DEBUG': 'True'
    }
    eph_options = EventHubStreamingClient.create_eventhub_eph_options(config, mock_logger)
    # Assert default config is returned.
    assert mock_logger.warning.called
    assert isinstance(eph_options, EPHOptions)
    assert eph_options.debug_trace

    mock_logger.reset_mock()

    # Pass in string and valid debug variable
    config = {
        'EVENT_HUB_EPH_OPTIONS': '{"debug_trace": "True"}',
        'EVENT_HUB_DEBUG': 'False'
    }
    eph_options = EventHubStreamingClient.create_eventhub_eph_options(config, mock_logger)
    # Assert default config is returned.
    assert not mock_logger.warning.called
    assert isinstance(eph_options, EPHOptions)
    # NOTE: EVENT_HUB_EPH_OPTIONS should overwrite EVENT_HUB_DEBUG
    assert eph_options.debug_trace

    mock_logger.reset_mock()

    # Pass in valid string
    config = {
        'EVENT_HUB_EPH_OPTIONS': '{"keep_alive_interval": "30"}'
    }
    eph_options = EventHubStreamingClient.create_eventhub_eph_options(config, mock_logger)
    # Assert default config is returned.
    assert not mock_logger.warning.called
    assert isinstance(eph_options, EPHOptions)
    assert eph_options.keep_alive_interval == 30

    mock_logger.reset_mock()

    # Pass in invalid string
    config = {
        'EVENT_HUB_EPH_OPTIONS': '{"keep_alive_interval": "True"}'
    }
    eph_options = EventHubStreamingClient.create_eventhub_eph_options(config, mock_logger)
    # Assert default config is returned.
    assert mock_logger.warning.called
    assert isinstance(eph_options, EPHOptions)
    assert eph_options.keep_alive_interval is None

    mock_logger.reset_mock()

    # Pass in custom EPH Options
    eph_options = EPHOptions()
    eph_options.keep_alive_interval = "-1"
    eph_options.debug_trace = True
    config = {
        'EVENT_HUB_EPH_OPTIONS': eph_options,
        'EVENT_HUB_DEBUG': 'False'
    }
    eph_options = EventHubStreamingClient.create_eventhub_eph_options(config, mock_logger)
    # Assert default config is returned.
    assert not mock_logger.warning.called
    assert isinstance(eph_options, EPHOptions)
    # NOTE: EVENT_HUB_EPH_OPTIONS should overwrite EVENT_HUB_DEBUG
    assert eph_options.keep_alive_interval == "-1"
    assert eph_options.debug_trace
