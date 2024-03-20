from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bootstrap_servers: str = Field("kafka.kafka.svc.cluster.local:9092", env="BOOTSTRAP_SERVERS")
    collector_topic: str = Field("test", env="COLLECTOR_TOPIC")
    group_id: str = Field("group_test", env="GROUP_ID")
    anomaly_topic: str = Field("test2", env="ANOMALY_TOPIC")


settings = Settings()
