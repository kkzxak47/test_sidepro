from confluent_kafka import Consumer, KafkaError
# Updated import path
import json
from config import Config


from ml_model import logger
from ml_model.ml_models import Text2ImageModel


model_mapping = {
    'text2image': Text2ImageModel,
    # 'generate-description': GenerateDescriptionModel,
    # 'generate-text': GenerateTextModel,
}


def kafka_consumer():
    # Configure the consumer
    consumer_config = {
        'bootstrap.servers': Config.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'ml_models_consumer_group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False  # Disable auto-commit
    }

    # Create the consumer
    consumer = Consumer(consumer_config)

    # Subscribe to the topic
    consumer.subscribe(['text2image'])

    try:
        logger.info('Starting consumer')
        while True:
            # Poll for messages
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info('Reached end of partition')
                else:
                    logger.error(f'Error: {msg.error()}')
            else:
                # Process the message
                try:
                    message_data = json.loads(msg.value().decode('utf-8'))
                    logger.info(f'Received message: {message_data}')

                    # Process the message here (e.g., generate image from prompt)
                    # ...
                    # use case 1: {'task_id': '6720dee630e131069b2f7c1c', 'text': 'ooo', 'task_type': 'text2image'}
                    mapped_model = model_mapping[message_data['task_type']]
                    model = mapped_model(message_data)
                    model.run()

                    # Manually commit the offset to mark the message as processed and delete it
                    consumer.commit(msg)
                    logger.info(f'Processed and committed message: {message_data}')
                except json.JSONDecodeError:
                    logger.error(f'Failed to decode message: {msg.value()}')
                except Exception as e:
                    logger.error(f'Error processing message: {str(e)}')

    except KeyboardInterrupt:
        logger.info('Consumer stopped by user')
    finally:
        logger.info('Closing consumer')
        # Close the consumer
        consumer.close()


if __name__ == '__main__':
    kafka_consumer()