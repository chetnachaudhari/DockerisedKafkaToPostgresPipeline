import logging
import os
from pathlib import Path

from data_generator import FakeDataGenerator
from producer import Producer

from confluent_kafka import avro, KafkaError

ORDERS_TOPIC = os.environ.get('ORDERS_TOPIC')
NUM_PARTITIONS = os.environ.get('NUM_PARTITIONS')
NUM_REPLICAS = os.environ.get('NUM_REPLICAS')
NUM_MESSAGES = os.environ.get('NUM_MESSAGES')

logger = logging.getLogger(__name__)

def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))

class OrderProducer(Producer):

    key_schema = Path(f"{Path(__file__).parents[0]}/schemas/order_key.json").read_text()
    value_schema = Path(f"{Path(__file__).parents[0]}/schemas/order_value.json").read_text()
    key_schema = key_schema.replace('\n', '')
    value_schema = value_schema.replace('\n', '')

    def __init__(self):

        topic_name = ORDERS_TOPIC
        super().__init__(
            topic_name,
            key_schema=self.key_schema,
            value_schema=self.value_schema,
            num_partitions=NUM_PARTITIONS,
            num_replicas=NUM_REPLICAS
        )


    ## This function takes jsonified order object
    def run(self, order):

        logger.debug("Publishing to topic {}: {}".format(self.topic_name, order))
        self.producer.produce(
            topic=self.topic_name,
            key=self.time_millis(),
            value=order,
            on_delivery=delivery_report
        )

    def close(self):
        super(OrderProducer, self).close()


def publish_messages():

    producer = OrderProducer()
    faker = FakeDataGenerator()
    logger.info('Generating {} messages'.format(int(NUM_MESSAGES)))
    for counter in range(int(NUM_MESSAGES)):
        logger.info('Counter={}'.format(counter))
        try:
            data = faker.generate_json_payload()
            producer.run(order=data)
        except Exception as ke:
            logger.info("Exception occured while generating messages {}".format(
            ke
            ))

    producer.close()


if __name__ == '__main__':
    publish_messages()
