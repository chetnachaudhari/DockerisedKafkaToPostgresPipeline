import logging
import os
import time
from uuid import uuid4

from confluent_kafka import SerializingProducer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import StringSerializer

logger = logging.getLogger(__name__)

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
SCHEMA_REGISTRY_URL = os.environ.get('SCHEMA_REGISTRY_URL')

def order_to_dict(order, ctx):
    return dict(order_id=order.order_id,
                customer_id=order.customer_id,
                product_id=order.product_id,
                order_date=str(order.order_date),
                order_state=order.order_state,
                order_quantity=order.order_quantity)

class Producer:

    kafka_client = AdminClient({"bootstrap.servers": KAFKA_BROKER_URL})
    existing_topics = set(topic_list.topic for topic_list in iter(kafka_client.list_topics(timeout=10).topics.values()))

    def __init__(
            self,
            topic_name,
            key_schema,
            value_schema=None,
            num_partitions=1,
            num_replicas=1
    ):
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = int(num_partitions)
        self.num_replicas = int(num_replicas)

        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)
        else:
            logger.debug("Topic already exists: {}".format(self.topic_name))

        schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)
        # key_serializer = JSONSerializer(self.key_schema,
        #                                 schema_registry_client
        #                                      )
        value_serializer = AvroSerializer(schema_registry_client,
                                          self.value_schema
                                             )

        producer_conf = {'bootstrap.servers': KAFKA_BROKER_URL,
                         'key.serializer':  StringSerializer('utf_8'),
                         'value.serializer': value_serializer
                         }
        self.producer = SerializingProducer(producer_conf)

    def create_topic(self):
        logger.info("Creating Topic: {}".format(self.topic_name))
        futures = self.kafka_client.create_topics([
            NewTopic(topic=self.topic_name, num_partitions=self.num_partitions, replication_factor=self.num_replicas),
        ])
        for _, future in futures.items():
            try:
                future.result()
            except Exception as e:
                logger.info("Exception occured while creating a topic: {}".format(self.topic_name))
                pass


    def time_millis(self):
        return str(int(round(time.time() * 1000)))


    def close(self):
        self.producer.flush()


    def get_uuid(self):
        return str(uuid4())