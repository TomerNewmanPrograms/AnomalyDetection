from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bootstrap_servers: str = Field("kafka.kafka.svc.cluster.local:9092", env="BOOTSTRAP_SERVERS")
    topics: str = Field("test", env="RECEIVE_DATA_TOPICS")
    group_id: str = Field("group_test", env="GROUP_ID")


settings = Settings()
