import logging
import asyncio
import os
import socket

from confluent_kafka import Consumer, KafkaException, Producer

from settings import settings

conf = {
    "bootstrap.servers": settings.bootstrap_servers,
    "client.id": socket.gethostname(),
    "security.protocol": "SASL_PLAINTEXT",  # Specify the SASL protocol
    "sasl.mechanism": "PLAIN",  # Specify the SASL mechanism
    "sasl.username": "user1",  # Your Kafka username
    "sasl.password": os.getenv("password")  # Your Kafka password
}

producer = Producer(conf)
consumer = Consumer(conf)
consumer.subscribe(settings.collector_topic)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def calculate_anomaly(cpu, memory):
    pass


async def process_message(decoded_msg):
    logger.info("process message %s", decoded_msg)
    cpu, memory = decoded_msg["cpu"], decoded_msg["memory"]
    if cpu <= 0 or memory <= 0:
        logger.error("message does not valid %s", decoded_msg)
        return
    if await calculate_anomaly(cpu, memory):
        logger.info("sending message %s", decoded_msg)
        producer.produce(topic=settings.anomaly_topic, value=decoded_msg.encode("utf-8"))
        logger.info("sent message %s", decoded_msg)


async def main():
    while True:
        try:
            logger.info("polling")
            msg = consumer.poll(timeout=1.0)  # Poll for new messages

            if msg is None:
                continue

            if msg.error():
                logger.error(msg.error())

            decoded_msg = msg.value().decode("utf-8")
            logger.info("new message %s", decoded_msg)
            await process_message(decoded_msg)

        except (KeyError, KafkaException) as e:
            logger.error(e)

        except KeyboardInterrupt:
            logger.error("Consumer stopped by user.")
            consumer.close()
            break


logger.info("processor starts to run")
asyncio.run(main())
