import asyncio
import json
import logging
import socket
import time

import psutil
from confluent_kafka import Producer, KafkaException
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

from settings import settings

conf = {
    "bootstrap.servers": settings.bootstrap_servers,
    "client.id": socket.gethostname(),
}
admin_client = AdminClient({"bootstrap.servers": settings.bootstrap_servers})
producer = Producer(conf)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
sleep = int(settings.intervals)


async def create_topic_if_not_exists(topic):
    try:
        new_topic = NewTopic(topic=topic, num_partitions=1, replication_factor=1)
        admin_client.create_topics([new_topic])
        logger.info("created topic - %s", new_topic)
    except Exception as e:
        logger.error(e)


async def list_known_topics():
    try:
        topic_metadata = admin_client.list_topics()
        logger.info("Topics in the Kafka cluster:")
        for topic in topic_metadata.topics.values():
            logger.info(topic)
    except Exception as e:
        logger.error(e)


async def collect_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_stats = psutil.virtual_memory()

    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory_stats.percent,
        "memory_available": memory_stats.available,
    }


async def send_data(data, topic):
    try:
        producer.produce(topic, value=data.encode("utf-8"))
        producer.flush()
        logger.info("message sent! - %s", data)
    except KafkaException as e:
        logger.error("Error when sending data - %s", e)
        logger.error("Error, data is %s", data)


async def run_collector():
    while True:
        try:
            metrics = collect_metrics()
            data_to_send = {
                "id": settings.id,
                "metrics": metrics,
            }
            await send_data(json.dumps(data_to_send), settings.topic)
            logger.info("sleep - %s", sleep)
            await asyncio.sleep(sleep)
        except KeyboardInterrupt as e:
            logger.error(e)
            break

