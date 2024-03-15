import logging
import socket
import time

import psutil
from confluent_kafka import Producer, KafkaException

from settings import settings

conf = {
    "bootstrap.servers": settings.bootstrap_servers,
    "client.id": socket.gethostname(),
}

producer = Producer(conf)

logger = logging.getLogger(__name__)

COLLECTION_INTERVAL = settings.intervals


def collect_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_stats = psutil.virtual_memory()

    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory_stats.percent,
        "memory_available": memory_stats.available,
    }


def send_data(data):
    try:
        producer.produce(settings.topic, value=data)
        producer.flush()
        logger.info("message sent! - %s", data)
    except KafkaException as e:
        logger.error("Error when sending data - %s", e)
        logger.error("Error, data is %s", data)


def main():
    while True:
        metrics = collect_metrics()
        data_to_send = {
            "metrics": metrics,
        }
        send_data(data_to_send)
        time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
    main()
