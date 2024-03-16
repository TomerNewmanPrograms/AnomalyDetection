from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    intervals: str = Field("5", env="INTERVALS")
    bootstrap_servers: str = Field("my-release-kafka.kafka.svc.cluster.local", env="BOOTSTRAP_SERVERS")
    topic: str = Field("test", env="SEND_DATA_TOPIC")
    id: str = Field("123", env="ID")


settings = Settings()
