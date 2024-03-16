import logging

from confluent_kafka import Consumer, KafkaException

from settings import settings

conf = {
    "bootstrap.servers": settings.bootstrap_servers,
    "group.id": settings.group_id,
}

consumer = Consumer(conf)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

topics = settings.topics.split()
consumer.subscribe(topics)


def process_message(decoded_msg):
    pass


def main():
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
            process_message(decoded_msg)

        except (KeyError, KafkaException) as e:
            logger.error(e)

        except KeyboardInterrupt:
            logger.error("Consumer stopped by user.")
            consumer.close()
            break


if __name__ == "__main__":
    main()
