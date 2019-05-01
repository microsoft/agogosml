"""Event Hub Streaming Class Unit Tests"""

from unittest.mock import patch

import pytest

from agogosml.common.kafka_streaming_client import KafkaStreamingClient


@patch('agogosml.utils.logger.Logger')
def test_create_kafka_config(mock_logger):
    """Test the create kafka config method."""

    with pytest.raises(ValueError):
        kafka_config = KafkaStreamingClient.create_kafka_config({}, mock_logger)

    # Pass in base config
    user_config = {
        'KAFKA_ADDRESS': 'localhost'
    }
    kafka_config = KafkaStreamingClient.create_kafka_config(user_config, mock_logger)
    # Should return default config.
    assert not kafka_config['enable.auto.commit']

    # Pass in invalid user config
    user_config = {
        'KAFKA_ADDRESS': 'localhost',
        'KAFKA_CONFIG': None
    }
    kafka_config = KafkaStreamingClient.create_kafka_config(user_config, mock_logger)
    # Should return default config.
    assert not kafka_config['enable.auto.commit']

    # Pass in invalid user config
    user_config = {
        'KAFKA_ADDRESS': 'localhost',
        'KAFKA_CONFIG': 'invalid_string'
    }
    kafka_config = KafkaStreamingClient.create_kafka_config(user_config, mock_logger)
    # Should return default config.
    assert mock_logger.warning.called
    assert not kafka_config['enable.auto.commit']

    mock_logger.reset_mock()

    # Pass in empty user config
    user_config = {
        'KAFKA_ADDRESS': 'localhost',
        'KAFKA_CONFIG': '{}'
    }
    kafka_config = KafkaStreamingClient.create_kafka_config(user_config, mock_logger)
    assert not mock_logger.warning.called
    assert not kafka_config['enable.auto.commit']

    mock_logger.reset_mock()

    # Pass in valid user config
    user_config = {
        'KAFKA_ADDRESS': 'localhost',
        'KAFKA_CONFIG': {"client.id": "test"}
    }
    kafka_config = KafkaStreamingClient.create_kafka_config(user_config, mock_logger)
    assert not mock_logger.warning.called
    assert not kafka_config['enable.auto.commit']
    assert kafka_config['client.id'] == 'test'

    mock_logger.reset_mock()

    # Pass in valid user config
    user_config = {
        'KAFKA_ADDRESS': 'localhost',
        'KAFKA_CONFIG': '{"client.id": "test"}'
    }
    kafka_config = KafkaStreamingClient.create_kafka_config(user_config, mock_logger)
    assert not mock_logger.warning.called
    assert not kafka_config['enable.auto.commit']
    assert kafka_config['client.id'] == 'test'

    mock_logger.reset_mock()

    # Pass in valid user config
    user_config = {
        'KAFKA_ADDRESS': 'localhost',
        'KAFKA_CONFIG': '{"enabled.auto.commit": true}'
    }
    kafka_config = KafkaStreamingClient.create_kafka_config(user_config, mock_logger)
    # Should squash 'enabled.auto.commit' to library setting.
    assert not mock_logger.warning.called
    assert not kafka_config['enable.auto.commit']

    mock_logger.reset_mock()

    # Pass in valid user config
    user_config = {
        'KAFKA_ADDRESS': 'localhost',
        'KAFKA_CONFIG': '{"enabled.auto.commit": true}',
        'KAFKA_CONSUMER_GROUP': 'helloworld',
        'KAFKA_DEBUG': 'consumer'
    }
    kafka_config = KafkaStreamingClient.create_kafka_config(user_config, mock_logger)
    # Should squash 'enabled.auto.commit' to library setting.
    assert not mock_logger.warning.called
    assert mock_logger.debug.called
    assert not kafka_config['enable.auto.commit']
    assert kafka_config['group.id'] == 'helloworld'
    assert kafka_config['debug'] == 'consumer'

    mock_logger.reset_mock()

    # Pass in valid user config
    user_config = {
        'KAFKA_ADDRESS': 'localhost',
        'EVENTHUB_KAFKA_CONNECTION_STRING': 'localhost'
    }
    kafka_config = KafkaStreamingClient.create_kafka_config(user_config, mock_logger)
    # Should squash 'enabled.auto.commit' to library setting.
    assert not mock_logger.warning.called
    assert not mock_logger.debug.called
    assert not kafka_config['enable.auto.commit']
    assert kafka_config['client.id'] == 'agogosml'

    mock_logger.reset_mock()
